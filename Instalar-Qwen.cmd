@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Instalar.ps1"
    if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" tools\install_ollama.py
if errorlevel 1 (
    pause
    exit /b 1
)
pause
