import os
import webbrowser
import requests
import musicLibrary
import openai
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv
from datetime import date

# Load environment variables from jarvis.env
load_dotenv("jarvis.env")

# Initialize modules
recognizer = sr.Recognizer()
openai.api_key = os.getenv("OPENAI_API_KEY")
newsapi = os.getenv("NEWS_API_KEY")

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        print("OpenAI Error:", e)
        return "Sorry, I couldn't process that."

def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found in your library.")
    elif "news" in c:
        try:
            today = date.today()
            r = requests.get(
                f"https://newsapi.org/v2/everything?q=technology&from={today}&sortBy=popularity&apiKey={newsapi}"
            )
            if r.status_code == 200:
                articles = r.json().get('articles', [])[:5]
                for article in articles:
                    speak(article['title'])
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            print("News Error:", e)
            speak("Couldn't fetch news right now.")
    else:
        output = aiProcess(c)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        try:
            print("Recognizing wake word...")
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)
            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes, how can I help?")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)

                    if "exit" in command.lower() or "stop" in command.lower():
                        speak("Goodbye.")
                        break

                    processCommand(command)

        except Exception as e:
            print("Error:", e)
