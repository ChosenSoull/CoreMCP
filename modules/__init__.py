import os
from mcp.server import MCPServer
from pydantic import AnyHttpUrl
from mcp.server.auth.settings import AuthSettings

from . import subagent, agent_tools, search_web, fetch_data, calculate, knowledge
from .auth import SimpleEnvVerifier, RESOURCE_URL

mcp = MCPServer("ChosenSoulMCP",
    token_verifier=None,   
    auth=None,
)

if os.getenv("MCP_SECRET_KEY") is not None:
    mcp.token_verifier = SimpleEnvVerifier()
    mcp.auth = AuthSettings(
            issuer_url=AnyHttpUrl("http://0.0.0.0:8001"), 
            resource_server_url=AnyHttpUrl(RESOURCE_URL),
            required_scopes=["all"],
            validate_token_resource=True,
    )

mcp.tool()(search_web.search_web)
mcp.tool()(fetch_data.fetch_data)
mcp.tool()(calculate.calculate)
mcp.tool()(knowledge.get_knowledge)
mcp.tool()(knowledge.save_documents)

if os.getenv("USE_RUN_SUBAGENT_TOOL", "False") == "True":
    mcp.tool()(subagent.run_subagent)

if os.getenv("USE_AGENT_TOOLS", "False") == "True":
    mcp.tool()(agent_tools.run_command)
    mcp.tool()(agent_tools.list_directory)
    mcp.tool()(agent_tools.read_file)
    mcp.tool()(agent_tools.write_file)
    mcp.tool()(agent_tools.search_files)
    mcp.tool()(agent_tools.run_program)
    