import sys
import praw
import time
import requests
import discord
import asyncio
import logging
import logging.config
import botToken
import reddit_data

from os import path
LOGGING_CONFIG = path.join(path.dirname(path.abspath(__file__)), 'logger.conf') 
logging.config.fileConfig(LOGGING_CONFIG)
logger = logging.getLogger("ecchi_bot")
logger.info("Bot has been started")

# Server
pupki = None

# Channels
ecchi_channel = None

# Discord client object
client = discord.Client()

@client.event
async def on_ready():
    
    # Global variables
    global pupki
    global ecchi_channel
  
    # Set server by ID 
    pupki = client.get_guild(392581230891106306)

    # Set 'test_bot_channel' channel 
    ecchi_channel = client.get_channel(836447934241046558)

    # Information about bot 
    logger.info('Logged in as:    ' + client.user.name)
    logger.info('On server:    ' + pupki.name)

    # Starting reddit parser
    await start_reddit_bot(ecchi_channel)

def start_streams():
    submission_stream = (reddit.subreddit("ecchi").stream.submissions(pause_after=-1)
                         if True else [])
    return submission_stream

async def start_reddit_bot(channel):
    first = True
    submission_stream = start_streams()   

    while True:
        try:
            for submission in submission_stream:
                if submission is None:
                    break
                if first == False:
                    await channel.send(submission.url)
            first = False
            await client.change_presence(status=discord.Status.online)
            time.sleep(10)
        except KeyboardInterrupt:
            logger.error('KeyboardInterrupt exception')
            sys.exit(0)
        except Exception as e:
            logger.error('Error:', e)
            time.sleep(30)
            submission_stream = start_streams() 

# Authorization on Reddit
reddit = praw.Reddit(
        client_id=reddit_data.client_id,
        client_secret=reddit_data.client_secret,
        password=reddit_data.password,
        user_agent=reddit_data.user_agent,
        username=reddit_data.username,
    )

# BOT TOKEN
client.run(botToken.DISCORD_BOT_TOKEN)
