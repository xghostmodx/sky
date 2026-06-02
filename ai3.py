#!/bin/bash
# Quantum Voice AI Assistant for Kali Linux

# ```python
# Quantum Voice AI Assistant
# Install dependencies:
# pip install openai speechrecognition pyttsx3 pyaudio
# Linux mic support may require:
# sudo apt install portaudio19-dev python3-pyaudio
# Export API key:
# export OPENAI_API_KEY="your_api_key"

import os
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are QuantumCap, an advanced voice AI assistant for Kali Linux.
Specialties:
- Quantum mechanics
- Quantum computing
- Linux systems
- Cybersecurity education
- Scientific reasoning

Explain quantum theory clearly, accurately, and with scientific depth.
Keep responses useful and practical.
"""

# Initialize voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

# Optional voice selection
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)


def speak(text):
    print(f"\nQuantumCap: {text}\n")
    engine.say(text)
    engine.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return "Speech recognition service unavailable"


def ask_ai(prompt, history):
    history.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply


def main():
    speak("QuantumCap online. Ask me about quantum theory, Linux, or cybersecurity.")

    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_input = listen()

        if not user_input:
            speak("I did not catch that.")
            continue

        if "exit" in user_input.lower() or "shutdown" in user_input.lower():
            speak("Shutting down QuantumCap.")
            break

        response = ask_ai(user_input, conversation)
        speak(response)


if __name__ == "__main__":
    main()
#```

## Features

 Voice input built-in using microphone=built-in;
* Spoken AI responses
* Quantum physics and quantum computing expertise
* Linux/Kali support
* Scientific educational assistant mode
* Expandable for local models like Ollama for privacy

## Upgrade ideas

* Replace cloud AI with local LLMs
* Add Whisper for better speech recognition
* Integrate penetration testing tool explanations
* Add GUI dashboard with PyQt

