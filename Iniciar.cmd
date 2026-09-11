@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Preparando a primeira execucao. E necessario Python 3.11 ou superior.
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Instalar.ps1"
    if errorlevel 1 (
        echo Nao foi possivel concluir a instalacao. Consulte o README.
        pause
        exit /b 1
    )
)
".venv\Scripts\python.exe" launcher.py
if errorlevel 1 pause
