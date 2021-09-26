import os
from datetime import datetime as dt

import pafy
import cv2
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
DEFAULT_INTERVAL = os.getenv('DEFAULT_INTERVAL')
TRACK0_URL = os.getenv('TRACK0_URL')
TRACK1_URL = os.getenv('TRACK1_URL')
TRACK2_URL = os.getenv('TRACK2_URL')
TRACK3_URL = os.getenv('TRACK3_URL')

bot = commands.Bot(command_prefix='!')
SCREENSHOT_SAVE_LOCATION = os.getcwd()
url_dict = {
    'keynote-track': TRACK0_URL,
    'r0-track': TRACK0_URL,
    'r1-track': TRACK1_URL,
    'r2-track': TRACK2_URL,
    'r3-track': TRACK3_URL,
}
event_dict = {
    'keynote-track': None,
    'r0-track': None,
    'r1-track': None,
    'r2-track': None,
    'r3-track': None,
}

# ---------------------------------------
# Bot Initialization
# ---------------------------------------
@bot.event
async def on_ready():
    print('Screenshot bot is ready.')


# ---------------------------------------
# Capture function
# ---------------------------------------
@tasks.loop(minutes=float(DEFAULT_INTERVAL))
async def capture(ctx, channel):
    url = url_dict[channel]
    print(url)

    vPafy = pafy.new(url)
    play = vPafy.getbest()
    
    cap = cv2.VideoCapture(play.url)
    _, img = cap.read()

    now = dt.now()
    str_time = now.strftime("%Y%m%d_%H%M")
    path = f"{SCREENSHOT_SAVE_LOCATION}/Screenshots/{channel}_{str_time}.png"
    cv2.imwrite(path, img)
    await ctx.send(file=discord.File(path))
    cap.release()
    print(f'{str_time} screenshots taken')

# ---------------------------------------
# Check function
# ---------------------------------------
def is_from_discord_manager(ctx):
    return 'discord manager' in [role.name for role in ctx.message.author.roles]

# ---------------------------------------
# Command
# ---------------------------------------
@bot.command()
@commands.check(is_from_discord_manager)
async def interval(ctx, *, param=None):
    try:
        capture.change_interval(minutes=int(param))
        await ctx.send(f"Interval change to {int(param)} minutes")
    except (TypeError, ValueError):
        await ctx.send("!interval needs a integer parameter that represents 'minutes'")

@bot.command()
@commands.check(is_from_discord_manager)
async def status(ctx, *, param=None):
    message = ""
    for name, event in event_dict.items():
        message += f"Screenshot on {name} is functioning: {bool(event) and not event.cancelled()}\n"
    await ctx.send(message)

@bot.command()
@commands.check(is_from_discord_manager)
async def start(ctx, *, param=None):
    channel = param if param != None else get_channel(ctx)
    print(channel)
    if channel in url_dict:
        event_dict[channel] = capture.start(ctx, channel)
        await ctx.send(f"{channel} screenshot start!")

@bot.command()
@commands.check(is_from_discord_manager)
async def stop(ctx, *, param=None):
    channel = param if param != None else get_channel(ctx)
    if channel in event_dict.keys():
        stop_event(event_dict, channel)
        await ctx.send(f"{channel} screenshot stop!")

def stop_event(event_dict, param):
    try:
        event = event_dict[param]
        event.cancel()
        event_dict[param] = None
    except Exception as e:
        print(e)

def get_channel(ctx):
    return str(ctx.message.channel)

bot.run(TOKEN)
