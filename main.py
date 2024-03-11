import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import * 
import youtube_dl
import yt_dlp
import asyncio


# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Command prefix
command_prefix = "!!"

# Bot setup
intents = Intents.default()
intents.voice_states = True
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

yt_dl_option = {"format" : "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_option)

ffmpeg = {"options" : "-vn"}


# Dictionary to store members and their requested YouTube URLs
default_video = "https://www.youtube.com/watch?v=aSzyI93e_zY"
url_video = ""
# members list = {user: [video, time]}
membersLIST = {}
default_player = FFmpegPCMAudio(ytdl.extract_info(default_video, download=False)['url'], **ffmpeg)
default_time = 10
# added this to update the member list every 2 min and give deafult intros for everyone
@tasks.loop(seconds=120)
async def make_defult_intro(bot_guilds):
    for i in bot_guilds:
        print("GUILD --> ", i)
        for j in i.members:
            if str(j) not in "intro_bot#8398":
                membersLIST[str(j)] = [default_player, default_time, ""]
    print("finshing creating defaults for everyone")

# @tasks.loop(seconds=120)
# async def make_defult_intro(bot_guilds):
#     for i in bot_guilds:
#         print("GUILD --> ", i)
#         for j in i.members:
#             if str(j) not in "intro_bot#8398":
#                 membersLIST[str(j)] = [default_player, default_time, ""]
#     #tmp = bot_guilds.member_count
#     tmp = 42
#     print("this is tmp::: ", tmp)

@bot.event
async def on_ready():
    make_defult_intro.start(bot.guilds)

# Function to join voice channel and play music
@bot.event
async def join_voice_channel(channel, user_name):
    voice_client = await channel.connect()

    try:
        # player = FFmpegPCMAudio(ytdl.extract_info(membersLIST[user_name][0], download=False)['url'], **ffmpeg)
        # data = ytdl.extract_info(membersLIST[user_name], download=False)['url']
        # song = data['url']
        # player = FFmpegPCMAudio(song, **ffmpeg)
        
        voice_client.play(membersLIST[user_name][0])

        await asyncio.sleep(membersLIST[user_name][1])
        await voice_client.disconnect()

        # membersLIST[user_name][0] = FFmpegPCMAudio(ytdl.extract_info(membersLIST[user_name][0], download=False)['url'], **ffmpeg)

        if (membersLIST[user_name][2] != ""):
            player = FFmpegPCMAudio(ytdl.extract_info(membersLIST[user_name][2], download=False)['url'], **ffmpeg)
            membersLIST[user_name][0] = player
            print("updated")
        else: 
            default_player = FFmpegPCMAudio(ytdl.extract_info(default_video, download=False)['url'], **ffmpeg)
            membersLIST[user_name][0] = default_player
            print("in esle")

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
    url_video = url
    membersLIST[str(ctx.author)][2] = url_video
    # tmp_player = FFmpegPCMAudio(ytdl.extract_info(url_video, download=False)['url'], **ffmpeg)
    # membersLIST[user_name][0] = tmp_player
    # print("in esle")
    # membersLIST[str(ctx.author)[2]] = True
    await ctx.send(f"Theme set for {ctx.author.mention}")



# Run the bot
bot.run(TOKEN)
