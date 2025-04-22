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

try:
    with open("wissen.json", "r", encoding="utf-8") as f:
        wissen = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Fehler in der JSON-Datei: {e}")
    wissen = {}
    
# ==== Umgebungsvariablen & Logging ====
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Nur Warnungen und Fehler anzeigen
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Optional: oneDNN deaktivieren

logging.basicConfig(filename='error.log', level=logging.ERROR,
                    format='%(asctime)s %(levelname)s:%(message)s')

load_dotenv()

API_KEY = os.getenv("API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

WISSEN_DATEI = "wissen.json"
LOG_DATEI = "chat_log.txt"
USER_DATA_DATEI = "user_data.json"
FEEDBACK_DATEI = "feedback.json"

# ==== Google-Suche ====
def internet_suche(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
        response = requests.get(url)
        response.raise_for_status()  # Überprüft auf HTTP-Fehler
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
    except Exception as e:
        logging.error(f"Allgemeiner Fehler bei der Internet-Suche: {e}")
        return f"Allgemeiner Fehler: {str(e)}"

# ==== Logging und Speicherung ====
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

# ==== Dateioperationen ====
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

# ==== KI-Modell (Keras, ohne Warnung) ====
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(10,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# ==== Flask App ====
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

# ==== Antwortgenerator ====
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

    # Überprüfen, ob die Eingabe mit "suche nach" beginnt
    if eingabe.startswith("suche nach "):
        query = eingabe.replace("suche nach ", "").strip()
        results = internet_suche(query)
        return f"Hier sind die Ergebnisse für deine Suche:\n{results}"

    if matches:
        return f"Hallo {name}, {random.choice(wissen[matches[0]])}"

    return "Ich bin mir nicht sicher, kannst du das anders formulieren?"

if __name__ == '__main__':
    # Flask starten
    print("[INFO] Starte Flask-App...")
    webbrowser.open("http://127.0.0.1:5000")  # Öffnet den Browser auf localhost:5000
    app.run(debug=True, use_reloader=False)  # Deaktiviert das automatische Öffnen des Browsers durch Flask
