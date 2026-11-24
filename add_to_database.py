from dotenv import load_dotenv
load_dotenv()
from modules import knowledge, fetch_data as fetch
import os
import tkinter as tk
from tkinter import filedialog
import openpyxl
import argparse
from docx import Document
from pypdf import PdfReader
from pptx import Presentation

def parse_pptx(file_path: str) -> str:
    prs = Presentation(file_path)
    slides_md = []

    for idx, slide in enumerate(prs.slides, start=1):
        slide_parts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                text = shape.text_frame.text.strip()
                if text:
                    slide_parts.append(text)
            if shape.has_table:
                rows = []
                for row in shape.table.rows:
                    cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
                    rows.append("| " + " | ".join(cells) + " |")
                if rows:
                    header_sep = "| " + " | ".join(["---"] * len(shape.table.columns)) + " |"
                    rows.insert(1, header_sep)
                    slide_parts.append("\n".join(rows))

        if slide_parts:
            slides_md.append(f"## Слайд {idx}\n\n" + "\n\n".join(slide_parts))

    return "\n\n".join(slides_md)

def parse_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    pages_md = []
    for idx, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text and text.strip():
            pages_md.append(f"## Страница {idx}\n\n{text.strip()}")
    return "\n\n".join(pages_md)


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    parts = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style_name = para.style.name.lower() if para.style else ""
        if "heading 1" in style_name:
            parts.append(f"# {text}")
        elif "heading 2" in style_name:
            parts.append(f"## {text}")
        elif "heading 3" in style_name:
            parts.append(f"### {text}")
        else:
            parts.append(text)

    for table in doc.tables:
        rows = []
        for row in table.rows:
            cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]
            rows.append("| " + " | ".join(cells) + " |")
        if rows:
            header_sep = "| " + " | ".join(["---"] * len(table.columns)) + " |"
            rows.insert(1, header_sep)
            parts.append("\n".join(rows))

    return "\n\n".join(parts)


def parse_xlsx(file_path: str) -> str:
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheets_md = []

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        rows = []
        for row in sheet.iter_rows(values_only=True):
            if not any(cell is not None for cell in row):
                continue
            cells = [str(cell).strip().replace("\n", " ") if cell is not None else "" for cell in row]
            rows.append("| " + " | ".join(cells) + " |")

        if rows:
            col_count = rows[0].count("|") - 1
            header_sep = "| " + " | ".join(["---"] * max(1, col_count)) + " |"
            rows.insert(1, header_sep)
            sheets_md.append(f"## Лист: {sheet_name}\n\n" + "\n".join(rows))

    return "\n\n".join(sheets_md)


def select_and_upload():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_paths = filedialog.askopenfilenames(
        title="Выберите файлы для загрузки в базу знаний",
        filetypes=[("Все файлы", "*.*")],
    )

    if not file_paths:
        print("Файлы не выбраны.")
        return

    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()
        file_name = os.path.basename(path)
        print(f"Обработка файла: {file_name}...")

        try:
            if ext == ".pdf":
                content = parse_pdf(path)
            elif ext == ".docx":
                content = parse_docx(path)
            elif ext in (".xlsx", ".xlsm"):
                content = parse_xlsx(path)
            elif ext == ".pptx":
                content = parse_pptx(path)
            else:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

            if content.strip():
                markdown_doc = content.strip()
                knowledge.save_documents(markdown_doc)
                print(f"Успешно добавлен в базу: {file_name}")
            else:
                print(f"Файл пуст или не удалось извлечь текст: {file_name}")

        except Exception as e:
            print(f"Ошибка при обработке {file_name}: {e}")

def save_site(url: str) -> None:
    print(f"Загрузка страницы: {url}...")
    try:
        content = fetch.fetch_data(args.url, RAG=True)
        if content:
            knowledge.save_documents(content)
            print(f"Успешно добавлено в базу: {url}")
        else:
            print(f"Не удалось извлечь текст со страницы: {url}")
    except Exception as e:
        print(f"Ошибка при обработке URL {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script for adding various files to a database for an LLM")
    parser.add_argument(
        "--type",
        required=True,
        choices=["file", "url"],
        type=str.lower,
        help="Type of data source: 'file' or 'url'",
    )
    parser.add_argument("--url", required=False, help="Site URL (required when --type url is specified)")

    args = parser.parse_args()

    if args.type == "url":
        if not args.url:
            parser.error("--url обязателен при --type url")
        save_site(args.url)
    else:
        select_and_upload()
    