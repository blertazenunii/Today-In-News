import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get the key
api_key = os.getenv("NEWSAPI_KEY")

# Print to verify
print(f"My API key is: {api_key}")
