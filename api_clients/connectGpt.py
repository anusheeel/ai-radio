import requests
from dotenv import load_dotenv
import json
import os
#Load openrouter API Key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL ="airadio.pro"
YOUR_APP_NAME = "AI on Air"
def connect_ChatGPTViaOpenRouter(message):
  print("ChatGPT incoming...imaginethesoundof someone tuning manual dial of classic radio")
  response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
      "Authorization": f"Bearer {OPENROUTER_API_KEY}",
      "HTTP-Referer": f"{SITE_URL}", # Optional, for including your app on openrouter.ai rankings.
      "X-Title": f"{YOUR_APP_NAME}", # Optional. Shows in rankings on openrouter.ai.
    },
    data=json.dumps({
      "model": "openai/gpt-3.5-turbo-0613", # Optional
      "messages": [
      {
        "role": "user",
        "content": message
      }
    ]
      
    }))
  return response.json()


