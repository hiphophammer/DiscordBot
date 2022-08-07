import discord
from discord.ext import commands
import os

import lckStanding

bot = commands.Bot(command_prefix='')
myToken = os.environ.get('MY_TOKEN')

lck_standing = lckStanding()
team_emoji = {
    'GEN':  '<:gen:1005837152044720188>',
    'T1':   '<:T1:1005837620972101703>',
    'DK':   '<DK:1005837689699962961>',
    'DRX':  '<DRX:1005837766149541888>',
    'FB':   '<FB:1005838000833446032>',
    'HLE':  '<HLE:1005838157750743123>',
    'KDF':  '<KDF:1005838244082098337>',
    'KT':   '<KT:1005838301141405706>',
    'NS':   '<NS:1005838422138704034>',
    'LSB':  '<SB:1005838597477372014>'
              }

team_codes = {
    '젠지': 'GEN',
    'T1': 'T1',
    '리브 샌박': 'LSB',
    '담원 기아': 'DK',
    'KT': 'KT',
    'DRX': 'DRX',
    '광동': 'KDF',
    '프레딧': 'FB',
    '농심': 'NS',
    '한화생명': 'HLE'
}


@bot.event
async def on_ready():
    return


# 순위표
async def match_standing(channel):
    result = ['LCK 순위표:']
    for i in range(10):
        result.append(f'\n> {i+1} **{team_emoji[team_codes[lck_standing.teams[i].name]]}** {lck_standing.teams.wins}승 {lck_standing.teams.losses}패, 득실: {lck_standing.teams.difference}')
    await channel.send(result)


# 명령어
@bot.command(name="ㅇㄴㄱㄱ")
async def ping(ctx):
    await ctx.send('pong')


@bot.command(name="순위표")
async def standing(ctx):
    await match_standing(ctx)
    
    


@bot.command()
async def default():
    return

bot.run(myToken)
