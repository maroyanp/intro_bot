import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

#load our token from somehwre sage
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

#bot setup
intents = Intents.default()
intents.message_content = True

client = Client(intents = intents)

# message functianality
async def send_message(msg: Message, userMsg: str):
    if not userMsg:
        print('(USER MSG EMPTY AS intents were not enabled)')

        return
    
    # is_private = userMsg[0]
    # if is_private:  
    # the same is done below in 1 line
    
    if is_private := userMsg[0] == '?': 
        userMsg = userMsg[1:] # slice from question mark

        try:
            response = str(get_response(userMsg))
            await msg.author.send(response) if is_private else msg.channel.send(response)
        except Exception as e:
            print(e)
