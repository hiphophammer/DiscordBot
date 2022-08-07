import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix='')
myToken = os.environ.get('MY_TOKEN')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(name="ㅇㄴㄱㄱ")
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def default():
    return

bot.run(myToken)
