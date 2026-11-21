@echo off
setlocal

call venv\Scripts\activate.bat

echo === Starting MCP Server ===

python main.py

pause