# Copilot Instructions

## Tech Stack
- Language: [Python 3.14]
- All packages in requirements.txt

## Code Style
- **Formatting**: Always use tabs for indentation.
- **Naming**: Enforce `snake_case` for all functions, methods, and variables. Use `PascalCase` for classes.
- **Imports**: Group imports in 3 blocks separated by a blank line: standard library, external packages, internal modules.
- **Comments**: Do not add comments for obvious code. Only comment on tricky workarounds or business rules.

## Architecture & Code Quality
- **Separation of Concerns**: Keep business logic in services; never perform database or network I/O inside route handlers.
- **Configuration**: Always read configurations from environment variables (.env file) via config modules, never hardcode values.
- **Error Handling**: Use custom error classes. Never catch errors silently (`except: pass`).
- **Logging**: Use the project's central logger, do not use raw `print()`.
