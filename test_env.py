from dotenv import load_dotenv
import os

load_dotenv()

print("ENV LOADED")
print(os.getenv("AZURE_OPENAI_ENDPOINT"))