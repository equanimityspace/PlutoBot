from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# get environment variables
discord_bot_token=os.getenv("DISCORD_TOKEN")
google_ai_token=os.getenv("AI_API_TOKEN")
