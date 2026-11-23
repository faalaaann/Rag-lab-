import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Explain what a reverse proxy does.",
    config=types.GenerateContentConfig(
        system_instruction="You are a senior DevOps engineer. Answer strictly in 3 concise bullet points with CLI examples.",
        temperature=0.3,
    ),
)

print(response.text)