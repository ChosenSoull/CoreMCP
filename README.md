<h1 align="center">Core MCP</h1>

<div align="center">

![RepoStars](https://img.shields.io/github/stars/ChosenSoull/CoreMCP?style=for-the-badge&logo=github&logoColor=E0AAFE&labelColor=11002C&color=E0AAFE)
![SizeRepo](https://img.shields.io/github/repo-size/ChosenSoull/CoreMCP?style=for-the-badge&logo=github&logoColor=E0AAFE&labelColor=11002C&color=E0AAFE)
</div>

<div align="center">

![Commits](https://img.shields.io/github/commit-activity/m/ChosenSoull/ChosenSoull?style=for-the-badge&logo=github&logoColor=E0AAFE&labelColor=11002C&color=E0AAFE)
![Issues](https://img.shields.io/github/issues/ChosenSoull/CoreMCP?style=for-the-badge&logo=github&logoColor=E0AAFE&labelColor=11002C&color=E0AAFE)
![Contributors](https://img.shields.io/github/contributors/ChosenSoull/CoreMCP?style=for-the-badge&logo=github&logoColor=E0AAFE&labelColor=11002C&color=E0AAFE)


</div>

## Project

A basic MCP for everyone - lightweight (1500 tokens) and equipped with essential tools for any user, including a calculator, search, and RAG. If needed, agentic tools can be enabled, allowing for file operations (reading, viewing, editing, searching) as well as the execution of commands and run programs.

## Instalation

For Server

> [!WARNING]
> Check variable USE_AGENT_TOOLS to False, it's maybe safe.

```
git clone https://github.com/ChosenSoull/CoreMCP.git
cd CoreMCP
python main.py
```

For [`Claude code`](https://claude.com/product/claude-code)/[`Codex`](https://openai.com/en-US/codex/)/[`Pi`](https://pi.dev)
Or any harness add `--transport stdio`

> [!TIP]
> And check enviroment variable MCP_SECRET_KEY

```JSON
{
  "mcpServers": {
    "CoreMCP": {
      "command": "python",
      "args": [
        "main.py",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

## Settings

All settings in enviroment variable. 
You can define in `.env` file or if use docker in command or `docker-compose` file

| Variable | Default | Description
| --- | --- | --- |
| HOST | 127.0.0.1 | Default host for server use 0.0.0.0 |
| PORT | 44321 | Default use port for MCP server |
| MCP_RESOURCE_URL | http://127.0.0.1:44321 | If you use nginx change this to domain name server |
| MCP_SECRET_KEY | NONE | API key. If you open server for world, use this |
| USE_AGENT_TOOLS | False | Activate agent tools NONE SANDBOX. And If use Server pls no use this feature |
| USE_RUN_SUBAGENT_TOOL | False | Activate subagent tool. LLM can call agent for any tasks |
| OPENAI_API_KEY | NONE | Setting this if provider use this |
| OPENAI_BASE_URL | http://localhost:8080/v1/ | Change this on one's own provider llm |
| OPENAI_MODEL | NONE | You provider model |
| OPENAI_TEMPERATURE | 0.7 | if you need this change |
| OPENAI_MAX_TOKENS | 65535 | I'am dont know what write |
| OPENAI_TOP_P | 1.0 | |
| OPENAI_SEED | None | |
| EMBEDDING_MODEL | Qwen/Qwen3-Embedding-0.6B | Embedding model for RAG system |
| EMBEDDING_MODEL_BASE_URL | http:127.0.0.1:8081 | This is url for RAG system, used OpenAI API |
| EMBEDDING_MODEL_API_KEY | NONE | |
| DQUANT_DATABASE | ./dquant-database | Folder path for Dquant database, embeddings storage |

## Stars

> [!TIP]
> Support the repository with a star

<a href="https://www.star-history.com/?repos=ChosenSoull22%2FCoreMCP&type=date&legend=top-left">
 <picture>
   <source srcset="https://api.star-history.com/chart?repos=ChosenSoull/CoreMCP&type=date&theme=light&legend=top-left" />
   <source srcset="https://api.star-history.com/chart?repos=ChosenSoull/CoreMCP&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ChosenSoull/CoreMCP&type=date&legend=top-left" />
 </picture>
</a>

## Contributors

[![Contributors](https://contrib.rocks/image?repo=ChosenSoull/CoreMCP)](https://github.com/ChosenSoull/CoreMCP/graphs/contributors)