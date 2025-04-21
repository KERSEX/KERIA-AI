# KERS AI Alpha - Deutschsprachiger KI-Chatbot

Ein web-basierter KI-Chatbot mit moderner Benutzeroberfläche, entwickelt in Python mit Flask.

## Features

- 🌐 Modernes, responsives Web-Interface
- 🔍 Google-Suche Integration
- 💾 Feedback-System und Chat-Protokollierung
- 🎵 Sound-Effekte

## Technologien

- Python 3.10
- Flask
- HTML/CSS/JavaScript
- Google Custom Search API

## Installation

1. Klone das Repository
2. Installiere die Abhängigkeiten:
```bash
pip install -r requirements.txt
```

## Konfiguration (env optional)

Erstelle eine `.env` Datei mit: 
```
API_KEY=dein_google_api_key
SEARCH_ENGINE_ID=deine_search_engine_id
```

## Starten

Führe aus:
```bash
python main.py
```
Der Server startet auf Port 5000.

## Projektstruktur

```
├── main.py           # Hauptanwendung
├── templates/        # HTML Templates
├── static/          # Statische Dateien
├── wissen.json      # Wissensdatenbank
└── requirements.txt # Abhängigkeiten
```

## Features im Detail

### Chatbot
- Antworten aus der Wissensdatenbank
- Internetsuche bei unbekannten Fragen mit "Suche nach" wenn es eingerichtet ist
- Feedback-System

### Benutzeroberfläche
- Dunkles Design
- Animierte Buttons
- Responsive Layout
- Seitenleiste mit Zusatzinfos

## Entwickler

Entwickelt von WHO_KERS
Discord: kers_ex

## Lizenz

Alle Rechte vorbehalten
