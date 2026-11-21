import json
import re
from camoufox.sync_api import Camoufox
from markdownify import markdownify as md
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

def fetch_data(url: str, fetch_type: str = "text", RAG: bool = False) -> str | dict | None:
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
        with Camoufox(
            headless=True,
            geoip=True,
            i_know_what_im_doing=True,
        ) as browser:
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
            except PlaywrightTimeoutError:
                pass

            if fetch_type == "json":
                body_text = page.inner_text("body")
                return json.loads(body_text)

            clean_html: str = page.evaluate("""() => {
                const junk = document.querySelectorAll(
                    'script, style, nav, footer, header, noscript, iframe, aside, ' +
                    '[aria-hidden="true"], .mw-editsection, sup.reference, .reflist, ' +
                    '.navbox, #catlinks, .ambox, .mw-jump-link, .printfooter'
                );
                junk.forEach(el => el.remove());
                
                document.querySelectorAll('td[colspan], th[colspan]').forEach(cell => {
                    const span = parseInt(cell.getAttribute('colspan'), 10);
                    if (span > 1) {
                        cell.removeAttribute('colspan');
                        for (let i = 1; i < span; i++) {
                            cell.parentNode.insertBefore(cell.cloneNode(true), cell.nextSibling);
                        }
                    }
                });

                const mainContent = document.querySelector('#mw-content-text, main, article') || document.body;
                return mainContent ? mainContent.innerHTML : '';
            }""")

            markdown_text = md(
                clean_html,
                heading_style="ATX",
                bullets="-",
                strip=[
                    *(["a"] if RAG else []),
                    "img",
                    "svg"
                ],
            )

            markdown_text = re.sub(r"\n\s*\n+", "\n\n", markdown_text).strip()
            return markdown_text

    except json.JSONDecodeError as e:
        raise ValueError(f"Невалидный JSON со страницы {url}: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка Camoufox при загрузке {url}: {e}") from e
