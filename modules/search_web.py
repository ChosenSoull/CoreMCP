from ddgs import DDGS

def search_web(query: str, max_results: int = 5) -> list[dict]:
    """Search the web using DuckDuckGo and return a list of results. 
    Parameters
    ----------
    query: str
        Target query.
    max_results: int, optional
        max results in number
    Returns
    -------
    array results with result or [] if error
    """
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"), 
                    "url": r.get("href"), 
                    "snippet": r.get("body")
                })
    except Exception as e:
        print(f"Search error: {e}")
        
    return results
