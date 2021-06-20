import discord
import lckSchedule as ls
import os
import pandas as pd

myToken = os.environ.get('MY_TOKEN')
channelID = 634035246592950284  # 노인정 일반
schedule = ls.LckSchedule()
client = discord.Client()


@client.event
async def on_ready():
    # logged on
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    channel = message.channel  # get this channel info

    # if message.content.lower() == '$help' or message.content.lower() == '$commands':  # help: commands
    #     help_list = '명령어는 초성으로도 입력 가능\n오늘경기, 내일경기, @@경기 (예: 젠지경기)'
    #     await channel.send(help_list)

    if message.content == '다음젠지경기' or message.content == '다음GEN경기' or message.content == '다음젠지' or message.content == '다음 젠지':
        found_game, found_index = schedule.get_next_match('GEN')
        print('Found name game:\n', found_game)

        result = []
        if len(found_game) == 0:
            result.append('다음 게임이 없어용')
        else:
            for index, match in found_game.iterrows():
                result.append('다음 젠지 경기:')
                result.append('\n')
                result.append(str(found_game['date'][found_index].month) + '월 ')
                result.append(str(found_game['date'][found_index].day) + '일 ')
                result.append(found_game['weekday'].at[found_index] + ' ')
                result.append(str(found_game['date'][found_index].hour) + '시 ')
                result.append(found_game['first_team_tricode'].at[found_index])
                result.append(' vs ')
                result.append(found_game['second_team_tricode'].at[found_index])
        z = ''.join(result)
        await channel.send(z)

    # 오늘 경기
    if message.content == '오늘경기' or message.content == 'ㅇㄴㄱㄱ' or message.content == '오늘ㄴㄱㄴㄱ' or \
            '오늘 ㄴㄱㄴㄱ' in message.content or message.content == '오늘 경기':  # match today
        print('now: ', )
        today_past, today_live, today_future = schedule.get_todays_matches()
        result = ''
        if len(today_past) == 0 and len(today_live) == 0 and len(today_future) == 0:
            result += '오늘은 경기 없음!'
            # TODO 다음 경기 스케쥴 추가
        else:  # has matches today
            if len(today_past) != 0:  # already has past matches
                # TODO 아이콘 추가
                result += '지난 경기'
                for index, match in today_past.iterrows():
                    result += '\n'
                    result = result + match['weekday'] + ' ' + match['league'] + ' ' + str(match['date'].hour) + '시 ' + \
                             match['first_team_tricode'] + '(' + match['first_team_score'] + ') vs ' + \
                             match['second_team_tricode'] + '(' + match['second_team_score'] + ')'
                result += '\n'
            if len(today_live) != 0:  # there is a live match
                result += '진행 중인 경기'
                for index, match in today_live.iterrows():
                    result += '\n'
                    result = result + match['league'] + ' ' + match['first_team_tricode'] + ' vs ' + \
                             match['second_team_tricode'] + ' ' + match['game_number'] + '번째 세트'
                result += '\n'
            if len(today_future) != 0:
                result += '예정된 경기'
                for index, match in today_future.iterrows():
                    result += '\n'
                    result = result + match['weekday'] + ' ' + match['league'] + ' ' + str(match['date'].hour) + '시' \
                             + match['first_team_tricode'] + ' vs ' + match['second_team_tricode']
        await channel.send(result)

    if message.content == '오늘경기' or message.content == 'ㅇㄴㄱㄱ' or \
            '오늘 ㄴㄱㄴㄱ' in message.content or message.content == '오늘 경기':  # match today
        pass
    # ------- for debugging: prints all messages --------- #
    # if not message.author.bot: # do only if message is sent from user && is testMode
    #     print('message: ', message)
    #     print('message type: ', type(message.content))
    #     print('message content: ', message.content)


client.run(myToken)
