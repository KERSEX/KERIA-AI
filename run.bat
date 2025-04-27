@echo off
set "VENV_DIR=venv"
REM Ins Projektverzeichnis wechseln (Ort der Batch-Datei)
cd /d "%~dp0"
REM Prüfen, ob die virtuelle Umgebung bereits existiert
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [INFO] Virtuelle Umgebung wird mit Python 3.9 erstellt...
    python3.9 -m venv venv
)
REM Aktivieren der virtuellen Umgebung
echo [INFO] Virtuelle Umgebung wird aktiviert...
call "%VENV_DIR%\Scripts\activate.bat"
REM Anforderungen aus requirements.txt installieren
if exist requirements.txt (
    echo [INFO] requirements.txt gefunden, Abhängigkeiten werden installiert...
    pip install -r requirements.txt
) else (
    echo [WARNUNG] Keine requirements.txt gefunden – überspringe Paketinstallation.
)
REM OPTIONAL: Starte hier dein Python-Projekt
REM z.B. python main.py