import os
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("API key not found")

API_KEY = GROQ_API_KEY
client = Groq(api_key=API_KEY)

def ask_groq(prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    user_prompt = "Tell me india's current president."
    answer = ask_groq(user_prompt)
    print("Groq's Response:\n", answer)