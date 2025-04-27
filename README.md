# KERS AI Alpha - Deutschsprachiger KI-Chatbot - Windows

Ein web-basierter KI-Chatbot mit moderner Benutzeroberfläche, entwickelt in Python mit Flask.

## Features

- 🌐 Modernes, responsives Web-Interface
- 🔍 Google-Suche Integration
- 💾 Feedback-System und Chat-Protokollierung
- 🎵 Sound-Effekte

## Technologien

- Python 3.9
- Flask
- HTML/CSS/JavaScript
- Google Custom Search API

## Installation
Wenn dies noch nicht getan ist, lade Python 3.9 runter.                    
https://apps.microsoft.com/detail/9P7QFQMJRFP7?hl=neutral&gl=DE&ocid=pdpshare

Lade die .zip datei runter und entpacke diese.

## Konfiguration von Google Custom Search Optional
Besuche diese Website: https://programmablesearchengine.google.com/about/
Drücke "Jetzt Starten", dann "Hinzufügen".
Gebe der "Suchmaschine" einen beliebigen Namen, danach "Im gesamten Web suchen" und erstellen.
Nun sollte eine Bestätigung erscheinen, drücke nun auf "Anpassen".
Bei Basisdaten sollte nun die Suchmaschinen-ID stehen diese fügt du bei "SEARCH_ENGINE_ID=" ein.

Nun der API_KEY
Scrolle runter bis zu Programmatischer Zugriff und drücke "Jetzt Starten".
Nun fordere den Schlüssel bei den blauen Button an "Schlüssel anfordern", nun erscheint ein Fenster mit "Enter new project name" und benenne es beliebig und drücke auf Next.
Nachdem laden steht dort "SHOW KEY", drücke "SHOW KEY" und kopiere diesen Key bei "API_KEY=" ein.

Bearbeite die `.env` Datei mit einem Editor.
```
API_KEY=dein_google_api_key
SEARCH_ENGINE_ID=deine_search_engine_id
```

## Starten

Doppelklick auf die run.bat datei, diese erstellt automatisch einen venv in Python 3.9 und installiert die Abhängigkeiten.

Der Server startet dann auf den Port 5000 und auf Localhost:5000.

## Projektstruktur

```
📁 Projektverzeichnis
├── 📁 templates/             # HTML-Templates für die Benutzeroberfläche
├── 📁 static/                # Statische Dateien (Sound- und Bilderdateien)
├── 📁 models/                # KI-Modelle und zugehörige Dateien
├── 📁 venv/                  # Virtuelle Python-Umgebung
├── 📄 run.bat                # Start- und Installationsskript für die Anwendung
├── 📄 main.py                # Hauptanwendung
├── 📄 API.env                # Konfiguration für die Google Search API
├── 📄 wissen.json            # Wissensdatenbank
├── 📄 chat_log.txt           # Aufzeichnung der Chat-Interaktionen
├── 📄 error.txt              # Fehlerprotokolle
└── 📄 requirements.txt       # Python-Abhängigkeiten
``` 

## Features im Detail

### Chatbot
- Antworten aus der Wissensdatenbank und Modellen
- Internetsuche bei unbekannten Fragen mit "Suche nach" wenn es eingerichtet ist
- Feedback-System und merkt sich den Namen wenn "Mein Name ist [Name]"

### Benutzeroberfläche
- Dunkles Design
- Animierte Buttons
- Responsive Layout
- Seitenleiste mit Zusatzinfos

## Entwickler

Entwickelt von WHO_KERS
Discord: kers_ex

MADE IN GERMANY
## Lizenz

Alle Rechte vorbehalten
