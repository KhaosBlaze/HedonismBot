import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from secrets import *
from post_twitter import post_status 

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_message(message):
	if message.channel.id == CHANNEL_ID:
		msg_txt = message.content
		if message.author.id == 331985003644977153:
			post_status(msg_txt)
		msg_txt = msg_txt.lower()
		if 'stellaris' in msg_txt:
			docker_spinup('Stellar')
		elif 'sea of theives' in msg_txt:
			docker_spinup('SoT');

@bot.command(pass_context=True)
async def on_ready():
	print("Ready for Armming")

def docker_spinup(game):
	if game == 'SoT':
		print('Spinning up The SOT BOX')
	if game == 'Stellar':
		print('Spinning up the Starbomb')

bot.run(HEDONISM_KEY)
