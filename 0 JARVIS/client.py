import openai
import os
from dotenv import load_dotenv

# Load your OpenAI key
load_dotenv("jarvis.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message['content'])
