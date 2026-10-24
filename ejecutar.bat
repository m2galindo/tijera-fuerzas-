@echo off
chcp 65001 >nul
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo No encuentro Python. Instalalo desde https://www.python.org/downloads/
    echo y marca la casilla "Add Python to PATH".
    pause
    exit /b 1
)

if not exist .venv (
    echo Creando entorno virtual e instalando dependencias...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

python tijera_fuerzas.py %*
echo.
pause
