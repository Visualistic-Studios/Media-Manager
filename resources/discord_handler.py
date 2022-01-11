

import discord
from discord.ext import commands
from resources.config import settings_manager


settings = settings_manager()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')



async def send_message_to_channel(message):
    channel = bot.get_channel(settings.get_channel_id())
    await channel.send(message)