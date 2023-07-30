import csv
import random
import textbase
from textbase.message import Message
from textbase import models
import os
from typing import List

# Load your OpenAI API key
models.OpenAI.api_key = "enter api key"
# or from environment variable:
# models.OpenAI.api_key = os.getenv("OPENAI_API_KEY")

# Prompt for GPT-3.5 Turbo
SYSTEM_PROMPT = """You are chatting with an AI medical expert. Please ask any medical-related questions, and I'll provide you with accurate answers!
"""

# Set to store medical keywords
medical_keywords = set()

# Load medical keywords from mtsamples.csv
with open("mtsamples.csv", newline="", encoding="utf-8") as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        keywords = row["keywords"].lower().strip()
        if keywords:
            medical_keywords.update(keywords.split(","))

# Medical Knowledge Base (Sample Data)
medical_knowledge_base = {
    "covid": {
        "symptoms": "The symptoms of COVID-19 include fever, cough, shortness of breath, fatigue, body aches, loss of taste or smell, sore throat, and more. If you have any specific concerns or symptoms, please consult a healthcare professional for personalized advice.",
        "first_aid": "If you suspect you have COVID-19 or have been exposed to the virus, self-isolate, wear a mask, and seek medical advice immediately.",
    },
    "cancer": {
        "symptoms": "The symptoms of cancer can vary depending on the type and stage of cancer. Common symptoms include unexplained weight loss, persistent fatigue, lumps or swelling, changes in skin or moles, and difficulty swallowing. If you experience any concerning symptoms, consult a healthcare professional.",
        "first_aid": "First aid for cancer involves early detection and timely medical consultation. Regular screenings and healthy lifestyle choices can reduce the risk of certain cancers.",
    },
    "flu": {
        "symptoms": "The symptoms of flu (influenza) include fever, chills, cough, sore throat, body aches, fatigue, and more. Rest, hydration, and over-the-counter medications can help manage symptoms, but consult a doctor if symptoms worsen.",
        "first_aid": "If you have the flu, rest, drink plenty of fluids, and take over-the-counter medications to relieve symptoms. Seek medical attention if symptoms are severe or persist.",
    },
    # Add more medical conditions and their corresponding first aid and symptoms information as needed.
}

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
    # Your custom logic to handle medical-related questions and provide accurate answers.

    for condition, data in medical_knowledge_base.items():
        if condition in user_message:
            # If the medical condition is found in the user's message, provide first aid and symptoms information.
            first_aid = data.get("first_aid", "First aid information not available.")
            symptoms = data.get("symptoms", "Symptoms information not available.")
            bot_response = f"For {condition}, First Aid: {first_aid}. Symptoms: {symptoms}"
            return bot_response

    # If the medical condition is not found, provide a general response.
    bot_response = "I'm sorry, I don't have specific information on that medical condition. Please consult a healthcare professional for personalized advice."
    return bot_response
