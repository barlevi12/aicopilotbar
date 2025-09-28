import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a smart autonomous agent helping analyze data and respond accordingly."},
        {"role": "user", "content": "Analyze the latest news about Apple stock."}
    ]
)

print("\n🔍 Agent's Response:\n")
print(response["choices"][0]["message"]["content"])
