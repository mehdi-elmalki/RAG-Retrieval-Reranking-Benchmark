@echo off
REM Lance RAGNova Studio. Double-cliquez ou executez depuis le dossier du projet.
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3.12 -m venv .venv || (echo Python 3.12 introuvable. Installez-le depuis python.org & pause & exit /b 1)
  .venv\Scripts\python.exe -m pip install --upgrade pip
  .venv\Scripts\python.exe -m pip install -r requirements.txt || (pause & exit /b 1)
)
.venv\Scripts\python.exe -m streamlit run 05_Application\app.py
pause
