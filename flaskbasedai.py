import eel
import pyttsx3
import datetime
import random
import webbrowser
import os
import threading
import requests
import re
import wikipedia

# ----------- ENV VARIABLES -----------
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

# ----------- GEMINI AI -----------
from google import genai
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# ----------- TEXT TO SPEECH -----------
engine = pyttsx3.init()
engine.setProperty("rate", 174)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def talk(text):
    try:
        eel.DisplayMessage(str(text))
        engine.say(str(text))
        engine.runAndWait()
    except:
        print("Speech error.")

# ----------- GREETINGS -----------
@eel.expose
def handle_greeting(command):
    responses = {
        "hi": "Hello! How can I help you today?",
        "hello": "Hey there! What can I do for you?",
        "how are you": "I am great! How are you?",
        "what's up": "I'm here waiting to assist you!"
    }
    eel.DisplayMessage(responses.get(command, "I didn't understand that."))

@eel.expose
def greet_based_on_time():
    hour = datetime.datetime.now().hour
    if hour < 12:
        eel.DisplayMessage("Good Morning!")
    elif hour < 18:
        eel.DisplayMessage("Good Afternoon!")
    else:
        eel.DisplayMessage("Good Evening!")

# ----------- SMALL TALK -----------
@eel.expose
def initiate_chat():
    messages = [
        "Hi! What's on your mind?",
        "I'm here to chat with you!",
        "How can I make your day better?"
    ]
    eel.DisplayMessage(random.choice(messages))

@eel.expose
def tell_fun_fact():
    facts = [
        "Honey never spoils!",
        "A day on Venus is longer than its year!",
        "Octopuses have three hearts!"
    ]
    eel.DisplayMessage(random.choice(facts))

@eel.expose
def tell_time():
    eel.DisplayMessage(datetime.datetime.now().strftime("The time is %I:%M %p"))

@eel.expose
def tell_joke():
    jokes = [
        "Why don’t skeletons fight? They don’t have the guts!",
        "I once heard a joke about amnesia, but I forgot how it goes.",
    ]
    eel.DisplayMessage(random.choice(jokes))

# ----------- SONGS / SYSTEM ----------
@eel.expose
def play_song():
    songs = [
        "https://www.youtube.com/watch?v=SNcmsQTZUKw",
        "https://www.youtube.com/watch?v=roz9sXFkTuE",
        "https://www.youtube.com/watch?v=nFgsBxw-zWQ",
    ]
    webbrowser.open(random.choice(songs))

@eel.expose
def shutdown_system():
    talk("Shutting down.")
    os.system("shutdown /s /t 1")

@eel.expose
def restart_system():
    talk("Restarting system.")
    os.system("shutdown /r /t 1")

# ----------- NUMBER GUESS GAME -----------
@eel.expose
def start_guess_the_number():
    global number_to_guess, attempts
    number_to_guess = random.randint(1, 100)
    attempts = 0
    eel.DisplayMessage("Guess a number between 1 and 100.")

@eel.expose
def guess_number(guess):
    global number_to_guess, attempts
    attempts += 1

    if guess < number_to_guess:
        eel.DisplayMessage("Too low!")
    elif guess > number_to_guess:
        eel.DisplayMessage("Too high!")
    else:
        eel.DisplayMessage(f"Correct! You guessed it in {attempts} tries.")

# ----------- OPEN APPS ----------
@eel.expose
def open_google():
    eel.DisplayMessage("Opening Google...")
    webbrowser.open("https://www.google.com")

@eel.expose
def open_youtube():
    eel.DisplayMessage("Opening YouTube...")
    webbrowser.open("https://www.youtube.com")

@eel.expose
def open_chatgpt():
    eel.DisplayMessage("Opening ChatGPT...")
    webbrowser.open("https://www.chatgpt.com")

# ----------- TRANSLATION -----------
@eel.expose
def translate_text(text, target_language):
    try:
        from deep_translator import GoogleTranslator
        translated = GoogleTranslator(source="auto", target=target_language).translate(text)
        eel.DisplayMessage("Translated: " + translated)
    except:
        eel.DisplayMessage("Translation failed.")

# ----------- WEATHER ----------
@eel.expose
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric"
        data = requests.get(url).json()

        if data["cod"] == 200:
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            eel.DisplayMessage(f"Weather in {city}: {desc}, {temp}°C")
        else:
            eel.DisplayMessage("City not found.")
    except:
        eel.DisplayMessage("Weather error.")

# ----------- CALCULATOR ----------
@eel.expose
def calculate_expression(expr):
    try:
        expr = re.sub(r"[^0-9+\-*/(). ]", "", expr)
        result = eval(expr)
        eel.DisplayMessage("Result: " + str(result))
    except:
        eel.DisplayMessage("Invalid expression.")

# ----------- WIKIPEDIA ----------
@eel.expose
def tell_about(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        eel.DisplayMessage(summary)
    except:
        eel.DisplayMessage("Topic not found.")

# ----------- GEMINI AI CHAT ----------
@eel.expose
def have_conversation(text):
    try:
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=text
        )
        eel.DisplayMessage(response.text.strip())
    except Exception as e:
        eel.DisplayMessage("Gemini AI error.")
        print(e)

# ----------- FLASK THREAD ----------
def start_flask():
    from flask import Flask, jsonify
    app = Flask(__name__)

    @app.route("/api/test")
    def test():
        return jsonify({"message": "Flask OK"})

    app.run(debug=False, port=5001, threaded=True)

threading.Thread(target=start_flask).start()

# ----------- START EEL UI ----------
eel.init("templates")
eel.start("index.html", size=(900, 700))
