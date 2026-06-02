#!/bin/bash
# Simple Kali Linux AI Terminal Assistant
# Requires: pip install openai
# Set API key: export OPENAI_API_KEY="your_key_here"

import os
import subprocess
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a Kali Linux AI assistant.
Help with Linux commands, penetration testing tools, scripting, and troubleshooting.
Always prioritize safe, legal, and authorized security practices.
"""

def ask_ai(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

def run_command(command):
    try:
        result = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return e.output

def main():
    print("=== Kali Linux AI Assistant ===")
    print("Type 'exit' to quit")
    print("Type 'run: <command>' to execute shell commands")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == "exit":
            break
        
        elif user_input.startswith("run:"):
            cmd = user_input.replace("run:", "", 1).strip()
            print("\n[Executing Command]")
            output = run_command(cmd)
            print(output)
        
        else:
            print("\n[AI Response]")
            answer = ask_ai(user_input)
            print(answer)

if __name__ == "__main__":
    main()
