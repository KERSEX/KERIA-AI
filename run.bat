@echo off
setlocal enabledelayedexpansion

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
    echo [WARNUNG] Keine requirements.txt gefunden.
    echo [WARNUNG] Müssen Installiert werden.
    pause
)

REM Prüfen, ob der Models-Ordner existiert
if exist "models\" (
    echo [INFO] Ordner 'models' gefunden.
    
    REM Prüfen, ob eine Datei mit "teuken" und ".gguf" existiert
    set "MODEL_FOUND=false"
    for %%F in ("models\teuken*.gguf") do (
        set "MODEL_FOUND=true"
        echo [INFO] Teuken-Modell gefunden: %%~nxF
    )
    
    if "!MODEL_FOUND!"=="true" (
        echo [INFO] Starte Python-Skript...
        python main.py
    ) else (
        echo [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
        echo [FEHLER] Keine teuken*.gguf Datei im models-Ordner gefunden!                    []
        echo [FEHLER] Bitte stellen Sie sicher, dass eine passende Modelldatei vorhanden ist.[]
        echo [FEHLER] Oder starte den Teuken Installer                                       [] 
        echo [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
        pause
        exit /b 1
    )
) else (
    echo [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
    echo [FEHLER] Ordner 'models' nicht gefunden!                                                  []
    echo [FEHLER] Bitte erstellen Sie den Ordner und fügen Sie die benötigten Modelldateien hinzu. []
    echo [][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
    pause
    exit /b 1
)

pause