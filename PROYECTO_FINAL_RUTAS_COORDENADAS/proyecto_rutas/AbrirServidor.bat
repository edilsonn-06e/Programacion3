@echo off
cd /d "%~dp0"
echo Iniciando servidor Flask...
start "" /b cmd /c "python app.py"
timeout /t 3 >nul
start http://127.0.0.1:5000
