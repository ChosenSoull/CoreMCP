from dotenv import load_dotenv
load_dotenv()

import os
from modules import mcp

def parse_port(port_str: str) -> int:
    try:
        port = int(port_str)
        if 1 <= port <= 65535:
            return port
        else:
            raise ValueError(f"Port {port} goes beyond the range (1-65535)")
            
    except ValueError as e:
        print(f"Error vilidation port: {e}")
        return 44321

DEFINE_HOST = os.getenv("HOST", "127.0.0.1")
DEFINE_PORT = os.getenv("PORT", "44321")

if __name__ == "__main__":
    print(f"MCP server for ChosenSoulMCP is ready. Starting on http://{DEFINE_HOST}:{DEFINE_PORT}")
    try:
        mcp.run(transport="sse", host=DEFINE_HOST, port=parse_port(DEFINE_PORT))
    except KeyboardInterrupt:
        print("Abnormal program termination")