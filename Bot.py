import os
import time
from datetime import datetime as dt

import pafy
import cv2
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
bot = commands.Bot(command_prefix='!', help_command=None)
SCREENSHOT_SAVE_LOCATION = os.getcwd()
url_dict = {
    'r1-peek': os.getenv('TRACK1_URL'),
    'r2-peek': os.getenv('TRACK2_URL'),
    'r3-peek': os.getenv('TRACK3_URL'),
    'test-peek': os.getenv('TRACK1_URL')
}
event_dict = {
    'r1-peek': None,
    'r2-peek': None,
    'r3-peek': None,
    'test-peek': None
}

# ---------------------------------------
# Bot Initialization
# ---------------------------------------
@bot.event
async def on_ready():
    print('Bot is ready.')


# ---------------------------------------
# Capture function
# ---------------------------------------
@tasks.loop(minutes=float(os.getenv('DEFAULT_INTERVAL')))
async def capture(ctx, channel):
    url = url_dict[channel]
    print(url)

    vPafy = pafy.new(url)
    play = vPafy.getbest()
    
    cap = cv2.VideoCapture(play.url)
    ret, img = cap.read()

    now = dt.now()
    str_time = now.strftime("%Y%m%d_%H%M")
    path = f"{SCREENSHOT_SAVE_LOCATION}/Screenshots/{channel}_{str_time}.png"
    cv2.imwrite(path, img)
    await ctx.send(file=discord.File(path))
    cap.release()
    print(f'{str_time} screenshots taken')


# ---------------------------------------
# Command
# ---------------------------------------
@bot.command()
async def interval(ctx, *, param=None):
    try:
        capture.change_interval(minutes=int(param))
        await ctx.send(f"Interval change to {int(param)} minutes")
    except (TypeError, ValueError):
        await ctx.send("!interval needs a integer parameter that represents 'minutes'")

@bot.command()
async def status(ctx, *, param=None):
    message = ""
    for name, event in event_dict.items():
        message += f"Screenshot on {name} is functioning: {bool(event) and not event.cancelled()}\n"
    await ctx.send(message)

@bot.command()
async def start(ctx, *, param=None):
    channel = param if param != None else get_channel(ctx)
    print(channel)
    if channel in url_dict:
        event_dict[channel] = capture.start(ctx, channel)
        await ctx.send(f"{channel} screenshot start!")

@bot.command()
async def stop(ctx, *, param=None):
    channel = param if param != None else get_channel(ctx)
    if channel in event_dict.keys():
        stop_event(event_dict, channel)
        await ctx.send(f"{channel} screenshot stop!")

def stop_event(event_dict, param):
    try:
        event = event_dict[param]
        event.cancel()
    except Exception as e:
        print(e)

def get_channel(ctx):
    return str(ctx.message.channel)

bot.run(os.getenv('TOKEN'))
