import discord
from discord.ext import commands
import logging
import asyncio
import os

import re
import random
import json

from config import config
from modules.dice import dice

#Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#Create config & checks
config = config()

#Ext List
extensions = {
    'modules.dice',
    'modules.admins'
}

#Create the bot client
client = commands.Bot(command_prefix='~')
for ext in extensions:
    client.load_extension(ext)

#Now we can setup the on-ready event
@client.event
async def on_ready():
    client.get_all_members()
    client.get_all_channels()

    print('Logged in...')
    print('------------')
    print('CONFIG:')
    print('Owner: ' + str(config.owner))
    print('Admins: ' + str(config.admins))
    print('------------')
    print('Have a lovely day <3')
    print('------------')
    print('')

@client.event
async def on_message(message):
    await client.wait_until_ready()
    if message.author.id == client.user.id:
        return

    channel = message.channel

    if channel.type == discord.ChannelType.private:
        return

    await client.process_commands(message)

client.run(config.botToken)