"""Data fetching functionality using Playwright."""
import json
import re
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright

class TagStripper(HTMLParser):
    """HTML parser that strips all tags and returns plain text."""
    
    def __init__(self):
        super().__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def get_text(self):
        return "".join(self.result)


def fetch_data(url: str, fetch_type: str = "text") -> str | dict | None:
    """Fetch a URL and return either raw text or parsed JSON.
    
    IMPORTANT: Use this tool *after* calling `search_web` to read the content 
    of a specific URL found in the search results when you need more details.

    Parameters
    ----------
    url: str
        Target URL.
    fetch_type: str, optional
        ``"text"`` to return the raw body, ``"json"`` to parse JSON.

    Returns
    -------
    str | dict | None
        The fetched content or ``None`` on failure.
    """
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ]
            )

            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.8059.40 Safari/537.36"
            )
            
            page = context.new_page()

            page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            page.goto(url, timeout=25000)

            page.wait_for_timeout(5000)
            
            if fetch_type == "json":
                body_text = page.inner_text("body")
                browser.close()
                return json.loads(body_text)
                
            html_content = page.content()
            browser.close()

            cleaned = re.sub(r'<(script|style|nav|footer|header|noscript|iframe)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

            parser = TagStripper()
            parser.feed(cleaned)

            raw_text = parser.get_text()
            clean_text = re.sub(r'\n\s*\n+', '\n\n', raw_text).strip()
            return clean_text
            
    except Exception as e:
        return f"Browser error fetching {url}: {e}"
