import eel
import pyttsx3
import datetime
import random
import webbrowser
import os
import threading
import time
from googletrans import Translator

# Initialize pyttsx3 engine for speech synthesis
engine = pyttsx3.init()

# Set voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # You can change index for different voices

# Function to make the assistant speak (non-blocking)
def talk(text):
    try:
        text = str(text)
        print(f"Speaking: {text}")  # Debug print
        engine.setProperty('rate', 174)
        engine.say(text)
        eel.DisplayMessage(text)  # Update message in frontend
        engine.runAndWait()
    except Exception as e:
        print(f"Error in talk function: {e}")

@eel.expose
def handle_greeting(command):
    greetings = {
        "hi": "Hello! How can I help you today?",
        "hello": "Hey there! What can I do for you?",
        "how are you": "I'm doing great, thank you for asking! How about you?",
        "what's up": "Not much, just here to assist you. What's up with you?"
    }
    
    response = greetings.get(command, "Sorry, I didn't quite get that. How can I assist you?")
    eel.DisplayMessage(response)

@eel.expose
def greet_based_on_time():
    hour = datetime.datetime.now().hour
    if hour < 12:
        eel.DisplayMessage("Good Morning! How can I assist you today?")
    elif 12 <= hour < 18:
        eel.DisplayMessage("Good Afternoon! How can I assist you today?")
    else:
        eel.DisplayMessage("Good Evening! How can I assist you today?")


@eel.expose
def initiate_chat():
    chats = [
        "Hello! How's your day going?",
        "Hi there! What would you like to talk about today?",
        "I'm feeling chatty! What's on your mind?",
        "Hey! Do you want to hear a fun fact?",
    ]
    eel.DisplayMessage(random.choice(chats))
import requests

@eel.expose
def tell_fun_fact():
    facts = [
        "Did you know? Honey never spoils. Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!",
        "Did you know? A day on Venus is longer than a year on Venus. It takes Venus 243 Earth days to rotate once but only 225 Earth days to orbit the Sun.",
        "Did you know? Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body."
    ]
    eel.DisplayMessage(random.choice(facts))  # Pick a random fact
            
@eel.expose
def tell_time():
    eel.DisplayMessage("The current time is : "+datetime.datetime.now().strftime('%I:%M %p'))

@eel.expose
def tell_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't eggs tell jokes? They might crack up."
    ]
    eel.DisplayMessage(random.choice(jokes))

@eel.expose
def play_song():
    # List of song links
    song_links = [
        "https://www.youtube.com/watch?v=SNcmsQTZUKw",
        "https://www.youtube.com/watch?v=roz9sXFkTuE",
        "https://www.youtube.com/watch?v=nFgsBxw-zWQ"
    ]
    
    # Select a random song from the list
    selected_song = random.choice(song_links)
    
    # Open the randomly selected song in the browser
    webbrowser.open(selected_song)

# Function to shut down the system
@eel.expose
def shutdown_system():
    talk("Shutting down your PC now.")
    os.system("shutdown /s /t 1")

@eel.expose
def restart_system():
    talk("Restarting your PC now.")
    os.system("shutdown /r /t 1")

# Example of function to start 'Guess the Number'

@eel.expose
def start_guess_the_number():
    global number_to_guess, attempts, game_over
    number_to_guess = random.randint(1, 100)  # Generate a number between 1 and 100
    attempts = 0
    game_over = False
    eel.DisplayMessage("Game started! Guess the number between 1 and 100.")  # Call JS function to update the message
@eel.expose
def open_google():
    webbrowser.open("https://www.google.com")
    eel.DisplayMessage("Opening Google...")

@eel.expose
def open_youtube():
    webbrowser.open("https://www.youtube.com")
    eel.DisplayMessage("Opening YouTube...")
@eel.expose
def open_chatgpt():
    webbrowser.open("https://www.chatgpt.com")
    eel.DisplayMessage("Opening chatgpt...")

@eel.expose
def translate_text(text, target_language='en'):
    try:
        translator = Translator()
        translated = translator.translate(text, dest=target_language)
        translated_text = translated.text
        eel.DisplayMessage(f"Translated text: {translated_text}")  # Send translated text back to frontend
    except Exception as e:
        eel.DisplayMessage(f"Error translating text: {e}")
import requests

API_KEY = "c0388506af3a1ab5d10d03e31e1cfc6a"  # Replace with your OpenWeatherMap API key

@eel.expose
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data['cod'] == 200:
            weather_desc = data['weather'][0]['description']
            temperature = data['main']['temp']
            eel.DisplayMessage(f"The weather in {city} is {weather_desc} with a temperature of {temperature}°C.")
        else:
            eel.DisplayMessage(f"Sorry, I couldn't fetch the weather for {city}.")
    except Exception as e:
        eel.DisplayMessage("There was an error fetching the weather.")
        

import re


@eel.expose
def calculate_expression(expression):
    try:
        
        expression = expression.lower()
        
        
        expression = re.sub(r'[^0-9+\-*/(). ]', '', expression)

        # Evaluate the expression safely
        result = eval(expression)

        # Display the result back to the frontend
        eel.DisplayMessage(f"The result is: {result}")
    except Exception as e:
        eel.DisplayMessage("Sorry, I couldn't calculate that. Please try again.")
        print(f"Error in calculation: {e}")


@eel.expose
def guess_number(guess):
    global number_to_guess, attempts, game_over
    attempts += 1
    if guess < number_to_guess:
        eel.DisplayMessage("Too low! Try again.")
    elif guess > number_to_guess:
        eel.DisplayMessage("Too high! Try again.")
    else:
        game_over = True
        eel.DisplayMessage(f"Congratulations! You've guessed the number in {attempts} attempts!")
        
import wikipedia

@eel.expose
def tell_about(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)  # Fetch a short summary of the topic
        eel.DisplayMessage(f"Here's what I found about {topic}: {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        eel.DisplayMessage(f"Sorry, there are multiple topics related to {topic}. Please be more specific.")
    except wikipedia.exceptions.HTTPTimeoutError:
        eel.DisplayMessage("Sorry, there was a timeout while fetching information. Please try again.")
    except Exception as e:
        eel.DisplayMessage(f"Sorry, I couldn't find any information about {topic}.")

# import openai

# openai.api_key = 'YOUR_OPENAI_API_KEY'  

# @eel.expose
# def have_conversation(user_input):
#     try:
#         response = openai.Completion.create(
#             engine="text-davinci-003",  # Choose the appropriate model
#             prompt=user_input,
#             max_tokens=150,  # Adjust response length
#             temperature=0.9,  # Control randomness of the response
#         )
#         reply = response.choices[0].text.strip()  # Get the assistant's response
#         eel.DisplayMessage(reply)  # Display the response in the frontend
#     except Exception as e:
#         eel.DisplayMessage("Sorry, I couldn't process your request. Please try again.")
#         print(f"Error: {e}")

# Flask initialization function
def start_flask():
    from flask import Flask, jsonify
    app = Flask(__name__)

    # Flask routes (if any)
    @app.route("/api/test", methods=["GET"])
    def test_route():
        return jsonify({"message": "Flask is running!"})

    app.run(debug=True, use_reloader=False, threaded=True)

# Start Flask in a separate thread
def start_flask_in_thread():
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

# Start Eel (the main UI logic)
eel.init('templates')  # Specify the directory containing the HTML and JS files

# Start Flask in a separate thread
start_flask_in_thread()

# Run the Eel frontend
eel.start('index.html', size=(800, 600))  # Start the Eel frontend
