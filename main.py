import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#load our token from somehwre sage
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)



