def calculate(expression: str) -> str:
    """Evaluate a simple arithmetic expression.

    The function performs a very small safety check: only digits, operators
    and parentheses are allowed.  For production use a proper parser should
    replace ``eval``.
    """
    allowed = set("0123456789.+-*/() ")
    if not set(expression).issubset(allowed):
        return "Error: expression contains disallowed characters."
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {e}"
