import json
import os
import uuid
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

DB_PATH = os.getenv("DQUANT_DATABASE", "./dquant-database")
COLLECTION_NAME = "knowledge_base"
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")

openai_client = OpenAI(
    api_key=os.getenv("EMBEDDING_MODEL_API_KEY", "not-needed"),
    base_url=os.getenv("EMBEDDING_MODEL_BASE_URL", "http://localhost:8081/v1"),
)
qdrant_client = QdrantClient(path=DB_PATH)

def _split_markdown(
    text: str,
    chunk_size: int = 2048,
    overlap: int = 300,
    max_size: int = 25000,
) -> list[str]:
    raw_blocks = [b.strip() for b in text.strip().split("\n\n") if b.strip()]
    blocks = []
    code_buffer = []
    in_code = False

    for rb in raw_blocks:
        fence_count = rb.count("```")
        if in_code:
            code_buffer.append(rb)
            if fence_count % 2 == 1:
                blocks.append("\n\n".join(code_buffer))
                code_buffer = []
                in_code = False
        else:
            if fence_count % 2 == 1:
                in_code = True
                code_buffer = [rb]
            else:
                blocks.append(rb)

    if code_buffer:
        blocks.append("\n\n".join(code_buffer))

    chunks = []
    current_chunk = ""

    for block in blocks:
        is_table = block.startswith("|") and "\n|" in block
        is_code = block.startswith("```")

        if (is_table or is_code) and len(block) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            if len(block) <= max_size:
                chunks.append(block)
            elif is_table:
                lines = block.splitlines()
                header = "\n".join(lines[:2]) if len(lines) >= 2 else ""
                body_lines = lines[2:] if len(lines) >= 2 else lines

                sub_chunk = header
                for line in body_lines:
                    if len(sub_chunk) + len(line) + 1 > max_size and sub_chunk != header:
                        chunks.append(sub_chunk.strip())
                        sub_chunk = f"{header}\n{line}" if header else line
                    else:
                        sub_chunk = f"{sub_chunk}\n{line}" if sub_chunk else line

                if sub_chunk and sub_chunk != header:
                    chunks.append(sub_chunk.strip())
            else:
                # Если код всё же больше max_size, режем по строкам без разрыва строк пополам
                lines = block.splitlines()
                sub_chunk = ""
                for line in lines:
                    if len(sub_chunk) + len(line) + 1 > max_size and sub_chunk:
                        chunks.append(sub_chunk.strip())
                        sub_chunk = line
                    else:
                        sub_chunk = f"{sub_chunk}\n{line}" if sub_chunk else line
                if sub_chunk:
                    chunks.append(sub_chunk.strip())
            continue

        if not (is_table or is_code) and len(block) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            step = max(1, chunk_size - overlap)
            for i in range(0, len(block), step):
                chunks.append(block[i : i + chunk_size].strip())
            continue

        if len(current_chunk) + len(block) + 2 > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                no_overlap_prev = current_chunk.rstrip().endswith("|") or current_chunk.rstrip().endswith("```")
                if not (is_table or is_code) and not no_overlap_prev and overlap > 0:
                    tail = current_chunk[-overlap:].lstrip()
                    current_chunk = f"{tail}\n\n{block}" if len(tail) + len(block) + 2 <= chunk_size else block
                else:
                    current_chunk = block
            else:
                current_chunk = block
        else:
            current_chunk = f"{current_chunk}\n\n{block}" if current_chunk else block

    if current_chunk:
        chunks.append(current_chunk.strip())

    cleaned_chunks = []
    for ch in chunks:
        if len(ch) < 50:
            is_atomic_prev = cleaned_chunks and (
                cleaned_chunks[-1].rstrip().endswith("|") or cleaned_chunks[-1].rstrip().endswith("```")
            )
            if cleaned_chunks and not is_atomic_prev and len(cleaned_chunks[-1]) + len(ch) + 2 <= chunk_size:
                cleaned_chunks[-1] = f"{cleaned_chunks[-1]}\n\n{ch}"
            continue
        cleaned_chunks.append(ch)

    return cleaned_chunks

def save_documents(text: str, batch_size: int = 32):
    """Saves text to a database using the RAG (Retrieval-Augmented Generation) method.
        Parameters
        ----------
        text : str
            Text that needs to be saved.
        Returns
        -------
        None (always)
    """
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
        )

    chunks = _split_markdown(text, chunk_size=1024)
    if not chunks:
        return

    points = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        response = openai_client.embeddings.create(input=batch, model=EMBEDDING_MODEL)
        
        for chunk, emb_data in zip(batch, response.data):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=emb_data.embedding,
                    payload={"text": chunk},
                )
            )

    for i in range(0, len(points), 500):
        qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points[i : i + 500])


def get_knowledge(question: str, top_k: int = 3) -> str:
    """Searches for and returns the top-k relevant text fragments from the database using the RAG (Retrieval-Augmented Generation) method.
        Parameters
        ----------
        question : str
            Text that needs to be saved.
        top_k : int (default: 3)
            Number of relevant responses.
        Returns
        -------
        str = answer from database in format JSON
    """
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        return json.dumps({"results": []}, ensure_ascii=False)

    query_vector = openai_client.embeddings.create(
        input=question, model=EMBEDDING_MODEL
    ).data[0].embedding

    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points

    results = [
        {"number": idx, "text": hit.payload["text"]}
        for idx, hit in enumerate(search_results, start=1)
        if hit.payload
    ]

    return json.dumps({"results": results}, ensure_ascii=False, indent=2)