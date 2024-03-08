import os
from dotenv import load_dotenv
from discord import *
from responses import get_response

# FIXMEEE 
membersLIST = {'Jake': "https://www.youtube.com/watch?v=YDAwLAoAeyw", 'why_yoshi' : "https://www.youtube.com/watch?v=KFU-_Ock6Pc"}

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
##ADDING IN COMMANDS FOR BOT
command_prefix = "!!"

# Create a bot instance with the specified command prefix
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

client = Client(intents = intents)

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
async def join_voice_channel(channel, UserName) -> None:
    # Fetch the channel object
    if channel:
        # Connect to the voice channel
        voice_client = await channel.connect()
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractor': 'youtube',
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(membersLIST[UserName], download=False)
                url = info['formats'][0]['url']
                voice_client.play(FFmpegPCMAudio(url), after=lambda e: print('done', e))
        
        except youtube_dl.DownloadError as e:    
            print(f"Error downloading audio: {e}")

    else:
        print("Channel not found.")



# adding in command for multiple users to have intros/ themes
@bot.command()
async def theme(ctx) -> None:
    if (ctx.message) != "" :
        print(ctx.message)
        print(membersLIST[ctx.author])
        
        #check if the user is not in member list
        if ctx.author not in membersLIST:
            membersLIST[ctx.author] = ctx.message
        else:
            #if user already in dict
            membersLIST[ctx.author] = ctx.message
    
    

client.run(token=TOKEN)
bot.run(token=TOKEN)