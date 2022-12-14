import discord
from legacy import lckSchedule_legacy as ls, lckStanding_legacy
import os
from discord.ext import tasks, commands
from datetime import datetime as dt
import requests
import datetime
import random
from PIL import Image

import pandas as pd
import numpy as np

myToken = os.environ.get('MY_TOKEN')
userToken = ''
channelID = 634035246592950284  # 노인정 일반
schedule = ls.LckSchedule()
standing = lckStanding_legacy.LckStanding()
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

# async def elden_ring(channel):
#     await channel.send(emoji_cat)
#     result = []
#     d_tday = datetime.datetime.now()
#     d1 = datetime.datetime(2022, 2, 25, hour=8)
#     delta = d1 - d_tday
#     if delta.seconds > 0:
#         hours = delta.seconds // 3600
#         minutes = (delta.seconds % 3600) // 60
#         seconds = delta.seconds % 60
#         result.append('출시까지 ' + str(delta.days) + '일' + str(hours) + '시간' + str(minutes) + '분' + str(seconds) + '초')
#     z = ''.join(result)
#     await channel.send(z)

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


@client.event
async def on_message(message):
    # ------- for debugging: prints all messages --------- #
    if not message.author.bot:  # do only if message is sent from user
        print('message: ', message)
        print('message type: ', type(message.content))
        print('message content: ', message.content)

    channel = message.channel  # get this channel info
    message_list = message.content.split(' ', 3)

    # message parsing
    if len(message_list) == 1 and not message.author.bot:
        if '만두' in message_list[0]:
            await send_gif(channel, message_list[0])
        elif '토코코' in message_list[0]:
            await send_gif(channel, message_list[0])
        elif message_list[0] == '모덩이':
            await send_gif(channel, "토코코01")
        elif '동물' in message_list[0] and '동물' != message_list[0]:
            await send_gif(channel, message_list[0])
        elif message_list[0] == '정말고마워요':
            await send_gif(channel, "동물01")
        elif message_list[0] == '그렇군요':
            await send_gif(channel, "동물02")
        elif message_list[0] == '참잘했어요':
            await send_gif(channel, "동물03")
        elif message_list[0] == '이상해요':
            await send_gif(channel, "동물04")
        elif message_list[0] == '싫은데요':
            await send_gif(channel, "동물05")
        elif message_list[0] == '어쩌라는거야':
            await send_gif(channel, "동물06")
        elif message_list[0] == '미안해요':
            await send_gif(channel, "동물07")
        elif message_list[0] == '됐어요':
            await send_gif(channel, "동물08")
        elif message_list[0] == '푸하하':
            await send_gif(channel, "동물09")
        elif message_list[0] == '잘자요':
            await send_gif(channel, "동물10")
        elif message_list[0] == '나빴어':
            await send_gif(channel, "동물13")
        elif message_list[0] == '으아아앙':
            await send_gif(channel, "동물14")
        elif message_list[0] == '먹을만하네요':
            await send_gif(channel, "동물15")
        elif message_list[0] == '반가워요':
            await send_gif(channel, "동물16")
        elif message_list[0] == '숨을래요':
            await send_gif(channel, "동물18")
        elif message_list[0] == '사랑해요':
            await send_gif(channel, "동물19")
        elif message_list[0] == '좋아해요':
            await send_gif(channel, "동물21")
        elif message_list[0] == '안아줘요':
            await send_gif(channel, "동물20")
        elif message_list[0] == '왜요':
            await send_gif(channel, "동물23")
        elif message_list[0] == '행복해요':
            await send_gif(channel, "동물24")
        elif message_list[0] == '지금가요':
            await send_gif(channel, "동물25")
        elif message_list[0] == '화났어요':
            await send_gif(channel, "동물27")
        elif message_list[0] == '할수있어요':
            await send_gif(channel, "동물28")
        elif message_list[0] == '졸려요':
            await send_gif(channel, "동물26")
        elif message_list[0] == '배고파요':
            await send_gif(channel, "동물32")
        elif message_list[0] == '변태':
            await send_gif(channel, "동물30")
        elif message_list[0] == '엘렐레' or message_list[0] == '앨랠래':
            await send_gif(channel, "동물22")
        elif message_list[0] == '어지러워요':
            await send_gif(channel, "동물33")
        elif message_list[0] == '저는기어다닐거에요' or message_list[0] == '저는기어다닐거예요':
            await send_gif(channel, "동물34")
        elif message_list[0] == '뭘봐요':
            await send_gif(channel, "동물35")
        elif message_list[0] == '두려워요':
            await send_gif(channel, "동물36")
        elif message_list[0] == '뱃속에고기가있어요':
            await send_gif(channel, "동물37")
        elif message_list[0] == '너무해요':
            await send_gif(channel, "동물38")
        elif message_list[0] == '뭐해요':
            await send_gif(channel, "동물39")
        elif message_list[0] == '지금가요':
            await send_gif(channel, "동물40")
        elif message_list[0] == '힘내요':
            await send_gif(channel, "동물41")
            #############
        elif message_list[0] == '페페그없':
            await send_gif(channel, message_list[0])
        elif message_list[0] == '냥겔라니움':
            await send_gif(channel, message_list[0])
        elif message_list[0] == '나나':
            await send_gif(channel, message_list[0])

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

        elif message_list[0] == 'ㅇㄷㄹ' or message_list[0] == '엘든링':
            await elden_ring(channel)

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
    elif '토코코' in txt:
        if txt[3:] == "01":
            folder = "tokoko"
            fname = "icon_1.gif"
    elif '동물' in txt:
        folder = "animal"
        if txt[2:] == "01":
            fname = "icon_1.png"
        elif txt[2:] == "02":
            fname = "icon_2.png"
        elif txt[2:] == "03":
            fname = "icon_3.png"
        elif txt[2:] == "04":
            fname = "icon_4.png"
        elif txt[2:] == "05":
            fname = "icon_5.png"
        elif txt[2:] == "06":
            fname = "icon_6.png"
        elif txt[2:] == "07":
            fname = "icon_7.png"
        elif txt[2:] == "08":
            fname = "icon_8.png"
        elif txt[2:] == "09":
            fname = "icon_9.png"
        elif txt[2:] == "10":
            fname = "icon_10.png"
        elif txt[2:] == "11":
            fname = "icon_11.png"
        elif txt[2:] == "12":
            fname = "icon_12.png"
        elif txt[2:] == "13":
            fname = "icon_13.png"
        elif txt[2:] == "14":
            fname = "icon_14.png"
        elif txt[2:] == "15":
            fname = "icon_15.png"
        elif txt[2:] == "16":
            fname = "icon_16.png"
        elif txt[2:] == "17":
            fname = "icon_17.png"
        elif txt[2:] == "18":
            fname = "icon_18.png"
        elif txt[2:] == "19":
            fname = "icon_19.png"
        elif txt[2:] == "20":
            fname = "icon_20.png"
        elif txt[2:] == "21":
            fname = "icon_21.png"
        elif txt[2:] == "22":
            fname = "icon_22.png"
        elif txt[2:] == "23":
            fname = "icon_23.png"
        elif txt[2:] == "24":
            fname = "icon_24.png"
        elif txt[2:] == "25":
            fname = "icon_25.png"
        elif txt[2:] == "26":
            fname = "icon_26.png"
        elif txt[2:] == "27":
            fname = "icon_27.png"
        elif txt[2:] == "28":
            fname = "icon_28.png"
        elif txt[2:] == "29":
            fname = "icon_29.png"
        elif txt[2:] == "30":
            fname = "icon_30.png"
        elif txt[2:] == "31":
            fname = "icon_31.png"
        elif txt[2:] == "32":
            fname = "icon_32.png"
        elif txt[2:] == "33":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_1.png"
        elif txt[2:] == "34":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_2.png"
        elif txt[2:] == "35":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_3.png"
        elif txt[2:] == "36":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_4.png"
        elif txt[2:] == "37":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_5.png"
        elif txt[2:] == "38":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_6.png"
        elif txt[2:] == "39":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_7.png"
        elif txt[2:] == "40":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_8.png"
        elif txt[2:] == "41":
            folder = os.path.join(folder, 'animal_dlc')
            fname = "icon_9.png"
    elif txt == '나나':
        folder = "nana"
        fname = "icon_" + str(random.randint(1, 45)) + ".gif"
    elif '페페그없' in txt:
        folder = "pepe"
        fname = "01.gif"
    elif '냥겔라니움' in txt:
        folder = "misc"
        fname = "1637094448.jpg"
    else:
        fname = "unknown.gif"
    fpath = os.path.join('resources', 'emojis', folder, fname)
    filename = "dccon"
    extension = ""
    if "gif" in fname:
        filename += ".gif"
        extension = ".gif"
    elif "png" in fname:
        filename += ".png"
        extension = ".png"
    elif "jpg" in fname:
        filename += ".jpg"
        extension = ".jpg"
    image = Image.open(fpath)
    image.thumbnail((100, 100))
    image.save("img" + extension)
    file = discord.File(("img" + extension), filename=filename)
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
