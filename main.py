import discord
import lckSchedule as ls
import lckStanding
import os

import pandas as pd
import numpy as np
import datetime

myToken = os.environ.get('MY_TOKEN')
channelID = 634035246592950284  # 노인정 일반
schedule = ls.LckSchedule()
standing = lckStanding.LckStanding()
client = discord.Client()


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
                         match['first_team_tricode'] + '(' + match['first_team_score'] + ') vs ' + \
                         match['second_team_tricode'] + '(' + match['second_team_score'] + ')'
            result += '\n'
        if len(today_live) != 0:  # there is a live match
            result += '진행 중인 경기'
            for index, match in today_live.iterrows():
                result += '\n'
                result += '> '
                result = result + match['league'] + ' ' + match['first_team_tricode'] + ' vs ' + \
                         match['second_team_tricode'] + ' ' + match['game_number'] + '번째 세트'
            result += '\n'
        if len(today_future) != 0:
            result += '예정된 경기'
            for index, match in today_future.iterrows():
                result += '\n'
                result += '> '
                result = result + match['weekday'] + ' ' + match['league'] + ' ' + str(match['date'].hour) + '시' + \
                         match['first_team_tricode'] + ' vs ' + match['second_team_tricode']
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
            result.append(found_game['first_team_tricode'].at[index])
            result.append(' vs ')
            result.append(found_game['second_team_tricode'].at[index])
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
            result.append(found_game['first_team_tricode'].at[found_index])
            result.append(' vs ')
            result.append(found_game['second_team_tricode'].at[found_index])
    z = ''.join(result)
    await channel.send(z)


@client.event
async def on_message(message):
    channel = message.channel  # get this channel info
    message_list = message.content.split(' ', 3)

    # message parsing
    if len(message_list) < 4:  # XX XX XX
        if message_list[0] == '다음' or message_list[0] == 'ㄷㅇ':
            try:
                if len(message_list) == 2 or message_list[2] == '경기':
                    if message_list[1] == '젠지' or message_list[1] == 'GEN' or message_list[1] == 'GEN.G':
                        await search_next_match(channel, 'GEN')
                    elif message_list[1] == '담원' or message_list[1] == 'DWG' or message_list[1] == 'DK':
                        await search_next_match(channel, 'DK')
                    elif message_list[1] == '한화' or message_list[1] == 'HLE' or message_list[1] == '한화생명':
                        await search_next_match(channel, 'HLE')
                    elif message_list[1] == '브리온' or message_list[1] == 'BRO' or message_list[1] == '프레딧브리온':
                        await search_next_match(channel, 'BRO')
                    elif message_list[1] == '아프리카' or message_list[1] == 'AF':
                        await search_next_match(channel, 'AF')
                    elif message_list[1] == '샌드박스' or message_list[1] == '샌박' or message_list[1] == '리브샌드박스':
                        await search_next_match(channel, 'LSB')
                    elif message_list[1] == 'KT' or message_list[1] == '케이티' or message_list[1] == '대퍼팀':
                        await search_next_match(channel, 'KT')
                    elif message_list[1] == '농심' or message_list[1] == 'NS':
                        await search_next_match(channel, 'NS')
                    elif message_list[1] == 'T1' or message_list[1] == '개좆슼' or message_list[1] == '티원' \
                            or message_list[1] == '대황슼' or message_list[1] == 'SKT' or message_list[1] == '그팀':
                        await search_next_match(channel, 'T1')
                    elif message_list[1] == 'DRX' or message_list[1] == '듀렉스' or message_list[1] == '콘돔':
                        await search_next_match(channel, 'DRX')
                    elif message_list[1] == '경기' or message_list[1] == 'ㄱㄱ':
                        await find_next_match(channel)
            except Exception as e:
                print('exception!', e)

        elif message_list[0] == 'ㄷㅇㄱㄱ':
            await find_next_match(channel)

        elif len(message_list) == 1 and (message_list[0] == 'ㅅㅇㅍ' or message_list[0] == '순위표'):
            await standing_whole_list(channel)

        elif cmd_is_today_match(message_list):
            current_time = '현재 시각: ' + str(
                pd.to_datetime(np.datetime64(datetime.datetime.now(), '[m]'), format='%Y-%m-%dT%H'))
            print(current_time)
            await channel.send('목록을 새로 고칩니다...')
            await today_match(channel)


async def standing_whole_list(channel):
    result = ['LCK 순위표:']
    for index, row in standing.result_df.iterrows():
        result.append('\n')
        result.append('> ')
        result.append(row['ranking'])
        result.append(' ')
        result.append('**')
        result.append(row['team_name'])
        result.append('**')
        result.append(' ')
        result.append(row['record'])
    z = ''.join(result)
    await channel.send(z)


def cmd_is_today_match(message_list):
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

    # ------- for debugging: prints all messages --------- #
    # if not message.author.bot: # do only if message is sent from user && is testMode
    #     print('message: ', message)
    #     print('message type: ', type(message.content))
    #     print('message content: ', message.content)


client.run(myToken)
