import os
from mcp.server.auth.provider import AccessToken, TokenVerifier

RESOURCE_URL = os.getenv("MCP_RESOURCE_URL","http://127.0.0.1:44321")
SECRET_KEY = os.getenv("MCP_SECRET_KEY")

class SimpleEnvVerifier(TokenVerifier):
    async def verify_token(self, token: str) -> AccessToken | None:
        KNOWN_TOKENS = {
            "ChosenSoul": AccessToken(token=SECRET_KEY, client_id="chosensoul", scopes=["all"], resource=RESOURCE_URL),
        }

        return KNOWN_TOKENS.get(token)