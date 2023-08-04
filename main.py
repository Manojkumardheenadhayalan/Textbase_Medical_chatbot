import csv
import random
import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List
import openai

# Load your OpenAI API key
models.OpenAI.api_key = "nil"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI medical expert. Please ask any medical-related questions, and I'll provide you with accurate answers!"""

# Set to store medical keywords
medical_keywords = set()

# Load medical keywords from mtsamples.csv
with open("mtsamples.csv", newline="", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        keywords = row["keywords"].lower().strip()
        if keywords:
            medical_keywords.update(keywords.split(","))

@textbase.chatbot("medical-bot")
def on_message(message_history: List[Message], state: dict = None):
    """Medical Expert Bot
    message_history: List of user messages
    state: A dictionary to store any stateful information

    Return a string with the bot_response or a tuple of (bot_response: str, new_state: dict)
    """

    if state is None or "counter" not in state:
        state = {"counter": 0}
    else:
        state["counter"] += 1

    # Get the user's latest message
    user_message = message_history[-1].content.lower()

    # Check if it's the first interaction with the bot
    if state["counter"] == 0:
        bot_response = "Hello! I'm an AI medical expert. How can I assist you with your medical-related questions?"
        state["counter"] += 1
    else:
        # Check if the user is asking a medical-related question
        if any(keyword in user_message for keyword in medical_keywords):
            # Process medical-related question and provide relevant response
            bot_response = process_medical_question(user_message)
        else:
            # Return a general response for non-medical queries
            bot_response = "I'm here to answer your medical-related questions. Please feel free to ask any health-related query."

    return bot_response, state

def process_medical_question(user_message: str) -> str:
    # Use the GPT-3.5 Turbo model to generate a response for the medical-related question.
    prompt = f"Medical question: {user_message}\n"
    response = openai.Completion.create(
        engine="text-davinci-002",  # You can use gpt-3.5-turbo here if you have access to it.
        prompt=prompt,
        max_tokens=150,
        api_key=models.OpenAI.api_key
    )
    bot_response = response['choices'][0]['text'].strip()
    return bot_response
