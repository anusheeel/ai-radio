import requests
from dotenv import load_dotenv
import json
import os
#Load openrouter API Key
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SITE_URL ="airadio.pro"
YOUR_APP_NAME = "AI on Air"
def connect_claude_via_openrouter(message):
    print("Claude incoming...imaginethesoundof someone tuning manual dial of classic radio")   
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": SITE_URL,  # Optional, for including your app on openrouter.ai rankings.
            "X-Title": YOUR_APP_NAME,  # Optional. Shows in rankings on openrouter.ai.
        },
        data=json.dumps({
            "model": "thedrummer/rocinante-12b",  # Optional
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        })
    )
    response.raise_for_status()  # Check for HTTP errors
    return response.json()

        
