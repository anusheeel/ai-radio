from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Print the loaded API key (ensure this is only for debugging and remove after)
print(f"Loaded API key: {os.getenv('OPENROUTER_API_KEY')}")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
