#!/bin/bash
# Kali Linux AI Chatbot
# Install:
# pip install openai colorama
# Export API key:
# export OPENAI_API_KEY="your_api_key"

import os
from openai import OpenAI
from colorama import Fore, Style, init

init(autoreset=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an advanced AI chatbot running on Kali Linux.
You help with:
- Linux commands
- Scripting
- Cybersecurity learning
- Troubleshooting
- General AI conversation

Always prioritize legal and ethical behavior.
"""

def chat():
    print(Fore.GREEN + "=== Kali Linux AI Chatbot ===")
    print(Fore.YELLOW + "Type 'exit' to quit.\n")

    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input(Fore.CYAN + "You: ")

        if user_input.lower() == "exit":
            print(Fore.RED + "Goodbye.")
            break

        conversation.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation
            )

            bot_reply = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": bot_reply})

            print(Fore.GREEN + "\nAI: " + Style.BRIGHT + bot_reply + "\n")

        except Exception as e:
            print(Fore.RED + f"Error: {e}")

if __name__ == "__main__":
    chat()
