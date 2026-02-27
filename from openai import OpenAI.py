from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Make a request
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a helpful network automation assistant."},
        {"role": "user", "content": "Generate a Python script to get router configuration using Netmiko."}
    ]
)

print(response.choices[0].message.content)
