"""MCP server for ChosenSoulMCP."""
from mcp.server import MCPServer

from . import search_web, fetch_data, calculate

mcp = MCPServer("ChosenSoulMCP")

mcp.tool()(search_web.search_web)
mcp.tool()(fetch_data.fetch_data)
mcp.tool()(calculate.calculate)
