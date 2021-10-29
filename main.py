import discord
import lckSchedule as ls
import lckStanding
import os
from discord.ext import tasks, commands
from datetime import datetime as dt
import requests
import datetime
import random

import pandas as pd
import numpy as np

myToken = os.environ.get('MY_TOKEN')
userToken = 'OTAyNDUzNDk3Njg4MTIxMzU1.YXepsw.9swHXOulpgVjbRAdZSm4cnt7xqM'
channelID = 634035246592950284  # 노인정 일반
comID = 902550990891401227
loaID = 902490387233505321
schedule = ls.LckSchedule()
standing = lckStanding.LckStanding()
last_checked_minute = 0
client = commands.Bot(command_prefix="#")

emoji_DK = '<:DK:856422574321434644>'
emoji_GEN = '<:GEN:856422574426554378>'
emoji_HLE = '<:HLE:856422574563917844>'
emoji_BRO = '<:FB:856422574158118943>'
emoji_AF = '<:AF:856422574325497856>'
emoji_LSB = '<:SB:856422574601535488>'
emoji_KT = '<:KT:856422574410170368>'
emoji_NS = '<:NS:856422574510702612>'
emoji_T1 = '<:T1:856420309098954772>'
emoji_DRX = '<:DRX:856422574329692170>'
emoji_soldier = '<:soldier:857954470604570655>'
emoji_cat = '<a:_cat_1:856502440567635968>'

commands = []  # 명령어 큐

emoji_cry = [
             '<:pepe_back:852087148303220786>',
             '<:pepe_cry:860868428838338591>',
             '<:pep_reflection:853643796256784454>',
             '<:cat7:852149097229058098>',
             '<:cat6:852148820137738300>',
             '<a:_pepe_sleep:856503214749122580>',
             '<:doge_weak:852091041879818240>',
             '<:cat1:823129249187495936>',
             '<:pepe_sadge:852091041879818240>',
             '<:pep:853643796193083402>',
             ]

wanderer_notice = ""

#     # 노인정
#     channel = client.get_channel(634035246592950284)
#
#     time_now = dt.now()
#     if time_now.minute % 10 == 9:
#         print('time: ', time_now, ', refreshing...')
#         standing.refresh()
#         schedule.refresh()
#         print('refreshed')
#
#     if time_now.minute == 0 and time_now.hour == 17:
#         past, current, future = schedule.get_todays_matches()
#         if not (len(past) == 0 and len(current) == 0 and len(future) == 0):
#             await channel.send('https://www.twitch.tv/lck_korea')
#             await today_match(channel)
#             await client.change_presence(activity=discord.Streaming(name="LCK", url="https://www.twitch.tv/lck_korea"))
#     elif client.activity is discord.Streaming:
#         contents = requests.get('https://www.twitch.tv/pikra10').content.decode('utf-8')
#         if 'isLiveBroadcast' not in contents:
#             standing.refresh()
#             schedule.refresh()
#             await client.change_presence(activity=discord.Game(name="칽"))


@client.event
async def on_ready():
    # logged on
    print('Logged in as {0.user}'.format(client))
    check.start()

@tasks.loop(seconds=1)
async def check():
    global last_checked_minute
    time_now = dt.now()
    print("checking... time_now: " + time_now.strftime('%m월 %d일 %H시 %M분 %S초'))
    if last_checked_minute != time_now.minute: # do every minute
        last_checked_minute = time_now.minute
        if time_now.minute == 55:
            await wipe_channel(client.get_channel(loaID))
            msg = ["> 다음 지역: \n"]
            if time_now.hour == 0:
                msg.append("> 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 1:
                msg.append("> 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 2:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부")
            elif time_now.hour == 3:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 4:
                msg.append("> 페이튼, 루테란 동부(2), 유디아, 애니츠, 슈샤이어, 루테란 서부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 5:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 6:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 7:
                msg.append("> 아르테미스, 루테란 동부(2), 유디아, 애니츠, 슈샤이어, 루테란 서부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 8:
                msg.append("> 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 9:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부")
            elif time_now.hour == 10:
                msg.append("> 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 11:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 12:
                msg.append("> 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 13:
                msg.append("> 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 14:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부")
            elif time_now.hour == 15:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 16:
                msg.append("> 페이튼, 루테란 동부(2), 유디아, 애니츠, 슈샤이어, 루테란 서부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 17:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 18:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 페이튼, 루테란 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 19:
                msg.append("> 페이튼, 루테란 동부(2), 유디아, 애니츠, 슈샤이어, 루테란 서부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 20:
                msg.append("> 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            elif time_now.hour == 21:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부")
            elif time_now.hour == 22:
                msg.append("> 페이튼, 루테른 동부, 유디아, 애니츠, 슈샤이어")
            elif time_now.hour == 23:
                msg.append("> 아르테미스, 욘, 베른 북부, 베른 남부, 루테란 서부, 루테란 동부, 토토이크, 아르데타인, 로헨델, 파푸니카")
            z = ''.join(msg)
            await client.get_channel(loaID).send(z)


async def today_match(channel):
    print('now: ', )
    today_past, today_live, today_future = schedule.get_todays_matches()
    result = ''
    print('fetched todays schedule')
    print('td_pst')
    print(today_past)
    print('td_live')
    print(today_live)
    print('td_future')
    print(today_future)
    no_match = False
    if len(today_past) == 0 and len(today_live) == 0 and len(today_future) == 0:
        print('no match today; searching for a future match...')
        result += '오늘은 경기 없음!'
        result += '\n'
        no_match = True
    else:  # has matches today
        if len(today_past) != 0:  # already has past matches
            # TODO 아이콘 추가
            result += '지난 경기'
            for index, match in today_past.iterrows():
                result += '\n'
                result += '> '
                result = result + match['weekday'] + ' ' + match['league'] + ' ' + str(match['date'].hour) + '시 ' + \
                         add_emoji(match['first_team_tricode']) + '(' + match['first_team_score'] + ') vs ' + \
                         add_emoji(match['second_team_tricode']) + '(' + match['second_team_score'] + ')'
            result += '\n'
        if len(today_live) != 0:  # there is a live match
            result += '진행 중인 경기'
            for index, match in today_live.iterrows():
                result += '\n'
                result += '> '
                result = result + match['league'] + ' ' + add_emoji(match['first_team_tricode']) + ' vs ' + \
                         add_emoji(match['second_team_tricode']) + ' ' + match['game_number'] + '번째 세트'
            result += '\n'
        if len(today_future) != 0:
            result += '예정된 경기'
            for index, match in today_future.iterrows():
                result += '\n'
                result += '> '
                result = result + match['weekday'] + ' ' + match['league'] + ' ' + str(match['date'].hour) + '시' + \
                         add_emoji(match['first_team_tricode']) + ' vs ' + add_emoji(match['second_team_tricode'])
    await channel.send(result)
    if no_match:
        await find_next_match(channel)


async def find_next_match(channel):
    found_game = schedule.get_next_match()
    print('Found game:\n', found_game)

    result = []
    if len(found_game) == 0:
        result.append('다음 게임이 없어용')
    else:
        result.append('다음 경기:')
        for index, match in found_game.iterrows():
            result.append('\n')
            result.append('> ')
            result.append(str(found_game['date'][index].month) + '월 ')
            result.append(str(found_game['date'][index].day) + '일 ')
            result.append(found_game['weekday'].at[index] + ' ')
            result.append(str(found_game['date'][index].hour) + '시 ')
            result.append(add_emoji(found_game['first_team_tricode'].at[index]))
            result.append(' vs ')
            result.append(add_emoji(found_game['second_team_tricode'].at[index]))
    z = ''.join(result)
    await channel.send(z)


async def search_last_game(channel):
    found_game, found_index = schedule.get_last_match()

    print('지난 경기:', found_game)
    result = []
    if len(found_game) == 0:
        result.append('지난 게임이 없어용')
    else:
        for index, match in found_game.iterrows():
            result.append('지난 경기:')
            result.append('\n')
            result.append('> ')
            result.append(str(found_game['date'][found_index].month) + '월 ')
            result.append(str(found_game['date'][found_index].day) + '일 ')
            result.append(found_game['weekday'].at[found_index] + ' ')
            result.append(str(found_game['date'][found_index].hour) + '시 ')
            if int(found_game['first_team_score'].at[found_index]) > int(
                    found_game['second_team_score'].at[found_index]):
                result.append('**')
            result.append(add_emoji(found_game['first_team_tricode'].at[found_index]))
            result.append('(' + found_game['first_team_score'].at[found_index] + ')')
            if int(found_game['first_team_score'].at[found_index]) > int(
                    found_game['second_team_score'].at[found_index]):
                result.append('**')
            result.append(' vs ')
            if int(found_game['first_team_score'].at[found_index]) < int(
                    found_game['second_team_score'].at[found_index]):
                result.append('**')
            result.append(add_emoji(found_game['second_team_tricode'].at[found_index]))
            result.append('(' + found_game['second_team_score'].at[found_index] + ')')
            if int(found_game['first_team_score'].at[found_index]) < int(
                    found_game['second_team_score'].at[found_index]):
                result.append('**')
    z = ''.join(result)
    await channel.send(z)


async def search_next_match(channel, team):
    found_game, found_index = schedule.search_for_next_match(team)
    print('Found game:\n', found_game)

    name_kr = ''
    if team == 'GEN':  # 1
        name_kr = '젠지'
    elif team == 'DK':  # 2
        name_kr = '담원'
    elif team == 'HLE':  # 3
        name_kr = '한화'
    elif team == 'BRO':  # 4
        name_kr = '브리온'
    elif team == 'AF':  # 5
        name_kr = '아프리카'
    elif team == 'LSB':  # 6
        name_kr = '리브 샌박'
    elif team == 'KT':
        name_kr = 'KT'
    elif team == 'NS':  # 8
        name_kr = '농심'
    elif team == 'T1':
        name_kr = 'T1'
    elif team == 'DRX':
        name_kr = 'DRX'

    result = []
    if len(found_game) == 0:
        result.append('다음 게임이 없어용')
    else:
        for index, match in found_game.iterrows():
            result.append('다음 ' + name_kr + ' 경기:')
            result.append('\n')
            result.append('> ')
            result.append(str(found_game['date'][found_index].month) + '월 ')
            result.append(str(found_game['date'][found_index].day) + '일 ')
            result.append(found_game['weekday'].at[found_index] + ' ')
            result.append(str(found_game['date'][found_index].hour) + '시 ')
            result.append(add_emoji(found_game['first_team_tricode'].at[found_index]))
            result.append(' vs ')
            result.append(add_emoji(found_game['second_team_tricode'].at[found_index]))
    z = ''.join(result)
    await channel.send(z)


async def animated_emoji(channel, message): # 움짤
    result = []
    result.append('<a:')
    print ('printing')
    if message == '모덩이':
        result.append('_mkk_dance:897626484796166244>')
    elif message == '페페펀치1':
        result.append('_pepe_punch01:854372448505561159>')
    elif message == '만두펀치':
        result.append('_misc_man2:853839945189163018>')
    z = ''.join(result)
    await channel.send(z)


async def han_degree(channel):
    contents = requests.get('https://hangang.ivlis.kr/aapi.php?type=dgr')
    await channel.send(emoji_cry[random.randint(0, 9)])
    await channel.send(contents.text)


async def quit_job(channel):
    print('희수 날짜 계산...')
    await channel.send(emoji_cat)
    result = []
    d_tday = datetime.date.today()
    d1 = datetime.date(2022, 2, 25)
    delta = d1 - d_tday
    if delta.days > 2:
        result.append('퇴사까지 ' + str(delta.days) + '일')
    elif delta.days == 1:
        result.append('퇴사까지 단 하루!!!')
    z = ''.join(result)
    await channel.send(z)

# async def eightsix(channel):
#     print('다음 에이티식스...')
#     await channel.send(emoji_cat)
#     result = []
#     d_tday = datetime.datetime.today()
#     d1 = datetime.datetime(2022, 2, 25)
#     delta = d1 - d_tday
#     if delta.days > 2:
#         result.append('퇴사까지 ' + str(delta.days) + '일')
#     elif delta.days == 1:
#         result.append('퇴사까지 단 하루!!!')
#     z = ''.join(result)
#     await channel.send(z)


async def wipe_channel(channel, msg = ""):
    async for m in channel.history():
        await m.delete()
    if msg != "":
        await channel.send(msg)

async def show_map(channel, txt):
    fname = "klee"
    if '아르테미스' in txt:
        if '로그' in txt:
            fname = '로그힐'
        elif '모스' in txt or '안게' in txt:
            fname = '안게모스'
        elif '국경' in txt:
            fname = '국경지대'
    elif '유디아' in txt:
        if '살란' in txt:
            fname = '살란드'
        elif '오즈' in txt:
            fname = '오즈혼'
    elif '루테란' in txt:
        if '서부' in txt:
            if '빌브' in txt:
                fname = '빌브린'
            elif '격전' in txt or '평야' in txt:
                fname = '격전의'
            elif '메드' in txt or '수도' in txt:
                fname = '메드리닉'
            elif '레이크' in txt:
                fname = '레이크바'
            elif '자고' in txt:
                fname = '자고라스'
        elif '동부' in txt:
            if '크로' in txt:
                fname = '크로커니스'
            elif '해무리' in txt:
                fname = '해무리'
            elif '보레아' in txt:
                fname = '보레아'
            elif '라이아' in txt:
                fname = '라이아'
            elif '흑장미' in txt:
                fname = '흑장미'
            elif '디오' in txt:
                fname = '디오리카'
            elif '배꽃' in txt:
                fname = '배꽃나무'
    elif '베른' in txt and '자베른' not in txt:
        if '남부' in txt:
            if '벨리' in txt:
                fname = '벨리온'
            elif '칸다' in txt:
                fname = '칸다리아'
        elif '북부' in txt:
            if '크로나' in txt:
                fname = '크로나'
            elif '파르나' in txt:
                fname = '파르나'
            elif '베르닐' in txt:
                fname = '베르닐'
            elif '발란' in txt:
                fname = '발란카르'
            elif '페스나르' in txt:
                fname = '페스나르'
    elif '토토이크' in txt:
        if '바다' in txt:
            fname = '바다향기'
        elif '달콤' in txt:
            fname = '달콤한'
        elif '성큼' in txt:
            fname = '성큼바위'
        elif '침묵' in txt:
            fname = '침묵하는'
    elif '애니츠' in txt:
        if '델파' in txt:
            fname = '델파이'
        elif '등나' in txt:
            fname = '등나무'
        elif '소리' in txt:
            fname = '소리의'
        elif '황혼' in txt:
            fname = '황혼의'
        elif '거울' in txt:
            fname = '거울'
    elif '아르데타인' in txt or '아르데' in txt:
        if '토트' in txt:
            fname = '토트리치'
        elif '메마' in txt:
            fname = '메마른'
        elif '갈라진' in txt:
            fname = '갈라진'
        elif '네벨' in txt:
            fname = '네벨호른'
        elif '바람' in txt:
            fname = '바람결'
        elif '리제' in txt:
            fname = '리제'
    elif '슈샤' in txt:
        if '얼어' in txt or '얼바' in txt:
            fname = '얼어붙은'
        elif '칼날' in txt:
            fname = '칼날바람'
        elif '서리' in txt:
            fname = '서리감옥'
        elif '머무른' in txt or '호수' in txt:
            fname = '머무른'
        elif '얼음' in txt:
            fname = '얼음나비'
    elif '로헨델' in txt:
        if '엘조' in txt or '그늘' in txt:
            fname = '엘조윈의'
        elif '은빛' in txt:
            fname = '은빛물결'
        elif '유리' in txt:
            fname = '유리연꽃'
        elif '바람' in txt or '호수' in txt:
            fname = '바람향기'
        elif '제나' in txt:
            fname = '파괴된'
    elif '욘' in txt:
        if '시작' in txt:
            fname = '시작의'
        elif '미완' in txt:
            fname = '미완의'
        elif '검은' in txt:
            fname = '검은모루'
        elif '무쇠' in txt:
            fname = '무쇠망치'
        elif '기약' in txt:
            fname = '기약의'
    elif '페이튼' in txt:
        fname = '칼라자 마을'
    elif '파푸니카' in txt:
        if '바닷길' in txt or '얕바' in txt:
            fname = '얕은'
        elif '별모' in txt:
            fname = '별모래'
        elif '티카' in txt:
            fname = '티카티카'
        elif '비밀' in txt or '비숲' in txt:
            fname = '비밀의'

    fpath = os.path.join('resources', 'wanderer_maps', fname)
    file = discord.File(fpath, filename="map.png")
    await channel.send("", file=file)


@client.event
async def on_reaction_add(reaction, user):
    if user.bot is False:
        print("reaction added, user is not bot")
        channel = reaction.message.channel
        if channel.id == loaID and reaction.emoji == "🗺️":
            print("added map reaction in 떠상 channel by user " + user.display_name)
            await show_map(channel, reaction.message.content)


@client.event
async def on_message(message):
    # ------- for debugging: prints all messages --------- #
    if not message.author.bot:  # do only if message is sent from user
        print('message: ', message)
        print('message type: ', type(message.content))
        print('message content: ', message.content)

    channel = message.channel  # get this channel info
    message_list = message.content.split(' ', 3)

    if channel.id == comID:
        target_chan = client.get_channel(loaID)
        lines = message.content.splitlines()
        result = []
        legen = False
        if len(lines) == 1:
            pass
        else:
            result += lines[0]
            result += " "
            result += lines[1]
            result += " "
            if "True" in lines[3]: # 웨이 뜸, 숭이들 다 부르기
                result += "웨이 "
                role = target_chan.guild.get_role(890387331524227093)
                result += role.mention
            else: # 웨이 안 뜸, 영호/전호 멘션
                if "전호" in lines[2]:
                    role = target_chan.guild.get_role(902726400463745054)
                    result += role.mention
                    legen = True
                else:
                    role = target_chan.guild.get_role(902726238844637234)
                    result += role.mention
        z = ''.join(result)
        msg = await target_chan.send(z)
        await msg.add_reaction("✅")
        await msg.add_reaction("🗺️")
        if legen:
            await msg.add_reaction("<:text_01:903195468127932446>")
            await msg.add_reaction("<:text_02:903195468350255125>")
            await msg.add_reaction("<:text_03:903195467972759573>")
            await msg.add_reaction("<:text_04:903195468169887764>")
            await msg.add_reaction("<:text_05:903195468065046549>")

    if not message.author.bot and channel.id == 902490387233505321:
        if len(message_list) == 1:
            if message_list[0] == '~영호':
                role = discord.utils.get(message.author.guild.roles, id=902726238844637234) # 영호롤
                await message.author.add_roles(role)
                await message.delete()
                await channel.send("<:mk_4:889863718748442654>")
            elif message_list[0] == '~전호':
                role = discord.utils.get(message.author.guild.roles, id=902726400463745054) # 전호롤
                await message.author.add_roles(role)
                await message.delete()
                await channel.send("<:mk_4:889863718748442654>")
            elif message_list[0] == "~wipe":
                await wipe_channel(channel)

    # message parsing
    elif len(message_list) == 1 and not message.author.bot:
        if '만두' in message_list[0]:
            await send_gif(channel, message_list[0])

    elif len(message_list) < 4 and not message.author.bot:  # XX XX XX
        if message_list[0] == '모덩이':
            await animated_emoji(channel, message_list[0])

        if message_list[0] == '다음' or message_list[0] == 'ㄷㅇ':
            try:
                if len(message_list) == 2 or message_list[2] == '경기':
                    if message_list[1] == '젠지' or message_list[1] == 'GEN' or message_list[1] == 'GEN.G' \
                            or message_list[1] == 'gen' or message_list[1] == 'geng' or message_list[1] == 'ㅈㅈ':
                        await search_next_match(channel, 'GEN')
                    elif message_list[1] == '담원' or message_list[1] == 'DWG' or message_list[1] == 'DK' \
                            or message_list[1] == 'dwg' or message_list[1] == 'ㄷㅇ':
                        await search_next_match(channel, 'DK')
                    elif message_list[1] == '한화' or message_list[1] == 'HLE' or message_list[1] == '한화생명' \
                            or message_list[1] == 'hle' or message_list[1] == 'ㅎㅎ':
                        await search_next_match(channel, 'HLE')
                    elif message_list[1] == '브리온' or message_list[1] == 'BRO' or message_list[1] == '프레딧브리온' \
                            or message_list[1] == '브로롱' or message_list[1] == 'bro' or message_list[1] == 'ㅂㄹㅇ':
                        await search_next_match(channel, 'BRO')
                    elif message_list[1] == '아프리카' or message_list[1] == 'AF' or message_list[1] == 'ㅇㅍㄹㅋ' \
                            or message_list[1] == 'ㅇㅍ':
                        await search_next_match(channel, 'AF')
                    elif message_list[1] == '샌드박스' or message_list[1] == '샌박' or message_list[1] == '리브샌드박스' \
                            or message_list[1] == 'ㅅㅂ' or message_list[1] == 'ㅅㄷㅂㅅ' or message_list[1] == 'ㅅㄷㅄ' \
                            or message_list[1] == 'sb' or message_list[1] == 'LSB' or message_list[1] == 'lsb' \
                            or message_list[1] == 'SB':
                        await search_next_match(channel, 'LSB')
                    elif message_list[1] == 'KT' or message_list[1] == '케이티' or message_list[1] == '대퍼팀' \
                            or message_list[1] == 'ㅋㅌ' or message_list[1] == 'ㅋㅇㅌ' or message_list[1] == 'kt':
                        await search_next_match(channel, 'KT')
                    elif message_list[1] == '농심' or message_list[1] == 'NS' or message_list[1] == 'ㄴㅅ' \
                            or message_list[1] == 'ns':
                        await search_next_match(channel, 'NS')
                    elif message_list[1] == 'T1' or message_list[1] == '개좆슼' or message_list[1] == '티원' \
                            or message_list[1] == '대황슼' or message_list[1] == 'SKT' or message_list[1] == '그팀' \
                            or message_list[1] == 'skt' or message_list[1] == 't1' or message_list[1] == 'ㅌㅇ':
                        await search_next_match(channel, 'T1')
                    elif message_list[1] == 'DRX' or message_list[1] == '듀렉스' or message_list[1] == '콘돔' \
                            or message_list[1] == 'drx':
                        await search_next_match(channel, 'DRX')
                    elif message_list[1] == '경기' or message_list[1] == 'ㄱㄱ':
                        await find_next_match(channel)
            except Exception as e:
                print('exception!', e)

        elif message_list[0] == 'ㅌㅅ' or message_list[0] == '퇴사':
            await quit_job(channel)

        elif message_list[0] == 'ㅎㄱ' or message_list[0] == '한강온도' or\
            message_list[0] == '한강수온':
            await han_degree(channel)

        elif message_list[0] == 'ㄷㅇㄱㄱ':
            await find_next_match(channel)

        elif message_list[0] == '새로고침' or message_list[0] == 'ㅅㄹㄱㅊ':
            await channel.send('새로 고치는 중...')
            standing.refresh()
            schedule.refresh()
            await channel.send('새로고침 완료!')

        elif message_list[0] == '지난경기' or message_list[0] == 'ㅈㄴㄱㄱ' or message_list[0] == '누가이김' \
                or message_list[0] == 'ㄴㄱㅇㄱ':
            await search_last_game(channel)

        elif message_list[0] == 'ㅈㄴ' or message_list[0] == '지난' or message_list[0] == '누가' or message_list[0] == 'ㄴㄱ':
            if len(message_list) == 2:
                if message_list[1] == '경기' or message_list[1] == 'ㄱㄱ' or message_list[1] == '이김' \
                        or message_list[1] == 'ㅇㄱ':
                    print('지난 경기')
                    await search_last_game(channel)

        elif len(message_list) == 1 and (message_list[0] == 'ㅅㅇㅍ' or message_list[0] == '순위표'):
            await standing_whole_list(channel)

        elif cmd_is_today_match(message_list):
            current_time = '현재 시각: ' + str(
                pd.to_datetime(np.datetime64(datetime.datetime.now(), '[m]'), format='%Y-%m-%dT%H'))
            print(current_time)
            await today_match(channel)


async def send_gif(channel, txt):
    fname = "unknown.gif"
    folder = "unknonwn"
    if '만두' in txt:
        if txt[2:] == "01":
            folder = "mandu"
            fname = "icon_1.gif"
        elif txt[2:] == "02":
            folder = "mandu"
            fname = "icon_2.gif"
        elif txt[2:] == "03":
            folder = "mandu"
            fname = "icon_3.gif"
        elif txt[2:] == "04":
            folder = "mandu"
            fname = "icon_4.gif"
        elif txt[2:] == "05":
            folder = "mandu"
            fname = "icon_5.gif"
        elif txt[2:] == "06":
            folder = "mandu"
            fname = "icon_6.gif"
        elif txt[2:] == "07" or txt[2:] == "펀치":
            folder = "mandu"
            fname = "icon_7.gif"
        elif txt[2:] == "08":
            folder = "mandu"
            fname = "icon_8.gif"
        elif txt[2:] == "09":
            folder = "mandu"
            fname = "icon_9.gif"
        elif txt[2:] == "10":
            folder = "mandu"
            fname = "icon_10.gif"
        elif txt[2:] == "12":
            folder = "mandu"
            fname = "icon_12.gif"
        elif txt[2:] == "13":
            folder = "mandu"
            fname = "icon_13.gif"
    else:
        fname = "unknown.gif"
    fpath = os.path.join('resources', 'emojis', folder, fname)
    file = discord.File(fpath, filename="dccon.gif")
    await channel.send("", file=file)


async def standing_whole_list(channel):
    result = ['LCK 순위표:']
    for index, row in standing.result_df.iterrows():
        result.append('\n')
        result.append('> ')
        result.append(row['ranking'])
        result.append(' ')
        result.append('**')
        result.append(add_emoji(row['team_name']))
        print(add_emoji(row['team_name']))
        result.append('**')
        result.append(' ')
        result.append(row['record'])
    z = ''.join(result)
    await channel.send(z)


def add_emoji(n):
    if n == 'T1':
        return emoji_T1 + n
    elif n == 'GEN' or n == 'Gen.G':
        return emoji_GEN + n
    elif n == 'DK' or n == 'DWG KIA':
        return emoji_DK + n
    elif n == 'HLE' or n == 'Hanwha Life Esports':
        return emoji_HLE + n
    elif n == 'BRO' or n == 'Fredit BRION':
        return emoji_BRO + n
    elif n == 'AF' or n == 'Afreeca Freecs':
        return emoji_AF + n
    elif n == 'LSB' or n == 'Liiv SANDBOX':
        return emoji_LSB + n
    elif n == 'KT' or n == 'kt Rolster':
        return emoji_KT + n
    elif n == 'NS' or n == 'NongShim REDFORCE':
        return emoji_NS + n
    else:
        return emoji_DRX + n


def cmd_is_today_match(message_list):
    print('is today match?:', message_list)
    if len(message_list) == 1:
        if message_list[0] == '오늘경기' or message_list[0] == 'ㅇㄴㄱㄱ' or message_list[0] == '오늘ㄴㄱㄴㄱ':
            return True
        else:
            return False
    elif len(message_list) == 2:
        if message_list[0] == '오늘' or message_list[0] == 'ㅇㄴ':
            if message_list[1] == '경기' or message_list[1] == 'ㄱㄱ' or message_list[1] == 'ㄴㄱ' or message_list[1] == '누구':
                return True
    elif len(message_list) == 3:
        if message_list[0] == '오늘' and message_list[1] == '경기':
            if message_list[2] == 'ㄴㄱ' or message_list[2] == '누구':
                return True
    return False


client.run(myToken)
