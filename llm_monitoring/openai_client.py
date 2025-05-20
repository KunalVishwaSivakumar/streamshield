# llm_monitoring/openai_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variable
load_dotenv(dotenv_path=".env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# ✅ Run test when called directly
if __name__ == "__main__":
    reply = ask_gpt("What is StreamShield?")
    print("🔹 GPT Reply:\n", reply)
