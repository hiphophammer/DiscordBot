import discord
from discord.ext import tasks, commands
import os

from lck_standing import LckStanding
from lck_schedule import LckSchedule


bot = commands.Bot(command_prefix='')
myToken = os.environ.get('MY_TOKEN')

lck_standing = LckStanding()

team_emoji = {
    'GEN': "<:GEN:1005835667038814208>",
    'T1': '<:T1:1005835670687862895>',
    'DK': '<:DK:856422574321434644>',
    'DRX': '<:DRX:856422574329692170>',
    'FB': '<:FB:1005835665554026526>',
    'HLE': '<:HLE:1005835559010304040>',
    'KDF': '<:KDF:1005835668708143134>',
    'KT': '<:KT:856422574410170368>',
    'NS': '<:NS:856422574510702612>',
    'LSB': '<:SB:856422574601535488>'
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
    print('Logged in.')


@tasks.loop(seconds=20.0)
async def update():
    # refresh standing
    lck_standing.refresh()
    # refresh schedule



# 순위표
async def match_standing(channel):
    result = ['LCK 순위표:']
    for i in range(10):
        team = lck_standing.teams[i]
        result.append('\n')
        result.append('> ')
        result.append(str(i+1))
        result.append(' ')
        result.append(team_emoji[team_codes[team.name]])
        result.append(' ')
        result.append(str(team.wins))
        result.append('승 ')
        result.append(str(team.losses))
        result.append('패 / 득실: ')
        result.append(str(team.difference))
    z = ''.join(result)
    await channel.send(z)


# 명령어
@bot.command(name="ㅇㄴㄱㄱ")
async def ping(ctx):
    await ctx.send('pong')


@bot.command(name="순위표")
async def standing(ctx):
    await match_standing(ctx)


@bot.command(name="ㅅㅇㅍ")
async def standing(ctx):
    await match_standing(ctx)


@bot.command()
async def default():
    return


bot.run(myToken)
