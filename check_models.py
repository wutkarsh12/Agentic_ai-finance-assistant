import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("🔍 Listing available models...\n")
for model in genai.list_models():
    print(f"Model name: {model.name}, methods: {model.supported_generation_methods}")
