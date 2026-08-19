import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def _get_client():
    api_key = os.getenv("GROQ_API_KEY") 
    return Groq(api_key=api_key)

def run_support_agent(user_message: str, user_email: str):
    system_prompt = f"""
    You are an AI support and billing assistant for our FastAPI & Stripe application.
    You are currently helping the user whose email is: {user_email}.
    Be polite, concise, and helpful.
    """

    
    client = _get_client()
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content