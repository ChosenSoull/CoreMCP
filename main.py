"""MCP server for ChosenSoulMCP."""
from modules import mcp

if __name__ == "__main__":
    print("MCP server for ChosenSoulMCP is ready. Starting on https://localhost:44321")
    try:
        mcp.run(transport="sse", host="localhost", port=44321)
    except KeyboardInterrupt:
        print("Аварийное завершение программы")