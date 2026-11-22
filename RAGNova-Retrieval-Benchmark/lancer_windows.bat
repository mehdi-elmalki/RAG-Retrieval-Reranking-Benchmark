
@echo off
setlocal
title RAGNova Studio - Lancement automatique
cd /d "%~dp0"

echo ====================================
echo       RAGNOVA STUDIO
echo ====================================

REM Verifier Python 3.12
py -3.12 --version
if errorlevel 1 goto erreur_python

REM Verifier l'environnement existant
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" --version >nul 2>&1
    if errorlevel 1 (
        echo Ancien environnement invalide.
        rmdir /s /q ".venv"
    )
)

REM Verifier que le venv utilise Python 3.12
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 12) else 1)"
    if errorlevel 1 (
        echo Ancien environnement incompatible.
        rmdir /s /q ".venv"
    )
)

REM Creer l'environnement si absent
if not exist ".venv\Scripts\python.exe" (
    echo Creation environnement Python 3.12...
    py -3.12 -m venv ".venv"
    if errorlevel 1 goto erreur
)

REM Installer les dependances
echo Verification des dependances...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erreur

REM Lancer RAGNova
echo.
echo Demarrage de RAGNova Studio...
".venv\Scripts\python.exe" -m streamlit run "05_Application\app.py"
if errorlevel 1 goto erreur
goto fin

:erreur_python
echo Python 3.12 introuvable.
goto erreur

:erreur
echo.
echo Une erreur est survenue.
pause
exit /b 1

:fin
pause
endlocal
