import os
from dotenv import load_dotenv
from discord import *
from responses import get_response

# FIXMEEE 
membersLIST = {'Jake': "https://www.youtube.com/watch?v=pvZJ8RDdlPI", 'why_yoshi' : "https://www.youtube.com/watch?v=YDAwLAoAeyw"}



# adding this for youtube playback
from discord.ext import commands
import youtube_dl
from discord import FFmpegPCMAudio

#load our token from somehwre sage
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

#bot setup
intents = Intents.default()
intents.message_content = True
intents.voice_states = True  # Enable voice state events


client = Client(intents = intents)

# message functianality
async def send_message(msg: Message, userMsg: str) -> None:
    if not userMsg:
        print('(USER MSG EMPTY AS intents were not enabled)')

        return None
    
    # is_private = userMsg[0]
    # if is_private:  
    # the same is done below in 1 line
    
    if is_private := userMsg[0] == '?': 
        userMsg = userMsg[1:] # slice from question mark

    try:
        response = str(get_response(userMsg))
        await msg.author.send(response) if is_private else await msg.channel.send(response)
    except Exception as e:
        print(e)

#handling startup for our bot
@client.event
async def on_read() -> None:
    print(client.user, "is now running")

#handiling incoming msgs
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return None
    
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username} : "{user_message}"')
    await send_message(message, user_message)


youtube_dl.utils.bug_reports_message = lambda: ''

# !!! CHECKING VOICE UPDATES
@client.event
async def on_voice_state_update(member, before, after) -> None:
    if before.channel != after.channel:  # Check if the user changed voice channels
        if after.channel:  # User joined a voice channel
            print(f'{member.display_name} joined {after.channel.name}')
            
            await join_voice_channel(after.channel, member.display_name)

        if before.channel:  # User left a voice channel
            print(f'{member.display_name} left {before.channel.name}')


@client.event
async def join_voice_channel(channel, UserName):
    # Fetch the channel object
    if channel:
        # Connect to the voice channel
        voice_client = await channel.connect()

        try:
            with youtube_dl.YoutubeDL() as ydl:
                info = ydl.extract_info(membersLIST[UserName], download=False)
                url = info['formats'][0]['url']
                voice_client.play(FFmpegPCMAudio(url), after=lambda e: print('done', e))
        
        except youtube_dl.DownloadError as e:    
            print(f"Error downloading audio: {e}")

    else:
        print("Channel not found.")


client.run(token=TOKEN)