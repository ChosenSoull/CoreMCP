@echo off
setlocal

cd /d "%~dp0"

set "PLAYWRIGHT_BROWSERS_PATH=%~dp0.ms-playwright"

call venv\Scripts\activate.bat

echo === Starting MCP Server ===

python main.py

pause