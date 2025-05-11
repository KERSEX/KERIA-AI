@echo off
setlocal

:: Zielordner festlegen (im gleichen Verzeichnis wie das Skript)
set "zielordner=%~dp0models"
set "dateiname=teuken-7b-instruct-commercial-v0.4-q8_0.gguf"
set "dateipfad=%zielordner%\%dateiname%"
set "downloadlink=https://huggingface.co/cristianadam/Teuken-7B-instruct-commercial-v0.4-Q8_0-GGUF/resolve/main/teuken-7b-instruct-commercial-v0.4-q8_0.gguf?download=true"

:: Zielordner erstellen, falls er nicht existiert
if not exist "%zielordner%" (
    mkdir "%zielordner%"
)
if exist "%dateipfad%" (
    echo Datei 'teuken-7b-instruct-commercial-v0.4-q8_0.gguf' gefunden.
)
 echo Wenn du nun fortfährst, wird die Datei 'teuken-7b-instruct-commercial-v0.4-q8_0.gguf' heruntergeladen und in den Ordner 'models' gespeichert. (7,93GB)
 echo Wenn die Datei runtergeladen wird 
 pause
:: Datei mit curl herunterladen
echo Lade Datei herunter... (Drücke STRG+C, um abzubrechen)
echo.

start "" /wait curl -L "%downloadlink%" -o "%dateipfad%"

:: Status ausgeben
if exist "%dateipfad%" (
    echo Download erfolgreich: %dateipfad%
) else (
    echo Fehler beim Download!
)
pause