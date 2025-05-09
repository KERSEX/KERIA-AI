import os
import logging
import json
import random
from datetime import datetime
import tensorflow as tf
from difflib import get_close_matches
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import webbrowser
from llama_cpp import Llama

# ==== Konfiguration ====
MODELL_VERZEICHNIS = "models/"
AKTUELLES_MODELL = "Teuken-7B-instruct-commercial-v0.4.Q6_K.gguf"  # Standardmodell

# ==== Logging & Umgebungsvariablen ====
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')
load_dotenv()

API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

WISSEN_DATEI = "wissen.json"
LOG_DATEI = "chat_log.txt"
USER_DATA_DATEI = "user_data.json"
FEEDBACK_DATEI = "feedback.json"

# ==== Modell laden ====
def lade_llm(modell_name):
    modell_pfad = os.path.join(MODELL_VERZEICHNIS, modell_name)
    if not os.path.exists(modell_pfad):
        print(f"[WARNUNG] ❌ Modell nicht gefunden: {modell_pfad}")
        # Modell nicht gefunden, mit Wissen aus der Datei weiterarbeiten
        print("[INFO] Nutze Wissen aus der 'wissen.json' Datei.")
        return None  # Kein Modell, aber Wissen kann weiterhin genutzt werden
    try:
        return Llama(
            model_path=modell_pfad,
            n_ctx=2048,
            n_threads=os.cpu_count() or 4,
            use_mlock=True
        )
    except Exception as e:
        print(f"[FEHLER] Fehler beim Laden des Modells: {e}")
        logging.error(f"Fehler beim Laden des Modells: {e}")
        return None

# Modell prüfen und auf Fehler reagieren
llm = lade_llm(AKTUELLES_MODELL)
if llm:
    print(f"[INFO] Modell '{AKTUELLES_MODELL}' erfolgreich geladen.")
else:
    print("[INFO] Das System läuft ohne Modell und nutzt stattdessen Wissen aus der 'wissen.json'.")


# ==== Modelle finden ====
def finde_modelle(pfad=MODELL_VERZEICHNIS):
    erlaubte_endungen = (".gguf", ".safetensors")
    return [f for f in os.listdir(pfad) if f.endswith(erlaubte_endungen)]

# ==== Wissen laden ====
try:
    with open(WISSEN_DATEI, "r", encoding="utf-8") as f:
        wissen = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Fehler in der JSON-Datei: {e}")
    wissen = {}

# ==== Flask App ====
app = Flask(__name__)

@app.route('/')
def index():
    try:
        modelle = finde_modelle()
        return render_template('index.html', modelle=modelle)
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Modelle: {e}")
        return "Fehler beim Laden der Modelle", 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('eingabe', '')
        response = antwort_generieren(user_input)
        log_chat(user_input, response)
        return jsonify({"antwort": response})
    except Exception as e:
        logging.error("Chat Error: %s", str(e))
        return jsonify({"error": "Ein Fehler ist aufgetreten."})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    results = internet_suche(query)
    return jsonify({"ergebnisse": results})

@app.route('/modell', methods=['POST'])
def modell_wechseln():
    global llm, AKTUELLES_MODELL
    try:
        data = request.json
        modell_name = data.get("modell")
        llm = lade_llm(modell_name)
        AKTUELLES_MODELL = modell_name
        return jsonify({"nachricht": f"✅ Modell '{modell_name}' erfolgreich geladen."})
    except Exception as e:
        logging.error(f"Fehler beim Modellwechsel: {e}")
        return jsonify({"nachricht": f"❌ Fehler: {str(e)}"}), 500

# ==== Funktionen ====
def internet_suche(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "items" in data:
            return "\n\n".join([
                f"{item['title']}\n{item.get('snippet', 'Keine Beschreibung verfügbar.')}\nLink: {item['link']}"
                for item in data['items'][:3]
            ]) or "Keine relevanten Ergebnisse gefunden."
        else:
            logging.error(f"Keine 'items' in der API-Antwort gefunden: {data}")
            return "Es wurden keine Ergebnisse gefunden."
    except requests.RequestException as e:
        logging.error(f"Fehler bei der Internet-Suche: {e}")
        return f"Fehler bei der Internet-Suche: {str(e)}"


def frage_llm(prompt):
    if llm is None:
        return "⚠️ Das Sprachmodell konnte nicht geladen werden. Bitte stelle sicher, dass es im models-Ordner liegt."
    try:
        response = llm(prompt, max_tokens=200, stop=["</s>"])
        return response["choices"][0]["text"].strip()
    except Exception as e:
        logging.error(f"LLM-Fehler: {e}")
        return "Es gab ein Problem beim Generieren der Antwort."

def antwort_generieren(eingabe):
    eingabe = eingabe.strip().lower()
    wissen = lade_wissen()
    matches = get_close_matches(eingabe, wissen.keys(), n=1, cutoff=0.6)
    name = lade_user_data().get("name", "Lebewesen")

    if eingabe.startswith("mein name ist "):
        name = eingabe.replace("mein name ist ", "").strip()
        speichere_name(name)
        return f"Hallo {name}, schön dich kennenzulernen!"

    if eingabe.startswith("feedback:"):
        speichere_feedback(eingabe, eingabe.replace("feedback:", "").strip())
        return "Danke für dein Feedback!"

    if eingabe.startswith("suche nach "):
        query = eingabe.replace("suche nach ", "").strip()
        results = internet_suche(query)
        return f"Hier sind die Ergebnisse für deine Suche:\n{results}"

    if matches:
        return f"Hallo {name}, {random.choice(wissen[matches[0]])}"

    return frage_llm(f"User: {eingabe}\nAssistant:")


def log_chat(eingabe, antwort):
    try:
        with open(LOG_DATEI, "a", encoding="utf-8") as log_file:
            log_file.write(f"{datetime.now()} - Du: {eingabe}\nKI: {antwort}\n\n")
    except Exception as e:
        logging.error(f"Fehler beim Loggen des Chats: {e}")


def speichere_feedback(eingabe, feedback):
    try:
        feedback_data = lade_feedback()
        feedback_data.append({"eingabe": eingabe, "feedback": feedback, "zeit": str(datetime.now())})
        with open(FEEDBACK_DATEI, "w", encoding="utf-8") as file:
            json.dump(feedback_data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Fehler beim Speichern des Feedbacks: {e}")


def lade_feedback():
    return json.load(open(FEEDBACK_DATEI, "r", encoding="utf-8")) if os.path.exists(FEEDBACK_DATEI) else []

def lade_user_data():
    return json.load(open(USER_DATA_DATEI, "r", encoding="utf-8")) if os.path.exists(USER_DATA_DATEI) else {}

def speichere_name(name):
    user_data = lade_user_data()
    user_data["name"] = name
    with open(USER_DATA_DATEI, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

def lade_wissen():
    return json.load(open(WISSEN_DATEI, "r", encoding="utf-8")) if os.path.exists(WISSEN_DATEI) else {}

# ==== App starten ====
if __name__ == '__main__':
    print("[INFO] Starte Flask-App...")
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True, use_reloader=False)