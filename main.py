import os
from dotenv import load_dotenv
from discord.ext import commands
from discord import * 
import youtube_dl
import yt_dlp


# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Command prefix
command_prefix = "!!"

# Dictionary to store members and their requested YouTube URLs
membersLIST = {'jake77': "https://www.youtube.com/watch?v=pvZJ8RDdlPI", 'shadowking111': "https://www.youtube.com/watch?v=YDAwLAoAeyw"}

# Bot setup
intents = Intents.default()
intents.voice_states = True
intents.message_content = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# yt_dl_option = {"format" : "bestaudio/best"}
# ytdl = yt_dlp.YoutubeDL(yt_dl_option)

# ffmpeg = {"options" : "-vn"}

# Function to join voice channel and play music
async def join_voice_channel(channel, user_name):
    voice_client = await channel.connect()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(membersLIST[user_name], download=False)
            url = info['formats'][0]['url']
            voice_client.play(FFmpegPCMAudio(url), after=lambda e: print('done', e))

    except youtube_dl.DownloadError as e:
        print(f"Error downloading audio: {e}")

# Event handler for voice state updates
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        if after.channel:
            print(f'{member.display_name} joined {after.channel.name}')
            await join_voice_channel(after.channel, str(member))

        if before.channel:
            print(f'{member.display_name} left {before.channel.name}')

# Adding command for users to set intros/themes
@bot.command()
async def theme(ctx, url: str):
    membersLIST[str(ctx.author)] = url
    await ctx.send(f"Theme set for {ctx.author.mention}")

# Run the bot
bot.run(TOKEN)
