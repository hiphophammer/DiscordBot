import discord
import lckSchedule as ls

myToken = 'Mjg1NjUxMTM3OTU5NTU5MTY4.WLO_Wg.tQOBIlY4j7jyXL7q3ylJhhnZJ0M'
schedule = ls.LckSchedule()
client = discord.Client()


@client.event
async def on_ready():
    # logged on
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    channel = message.channel  # get this channel info

    if message.content.lower() == '$help':  # help: commands
        help_list = '$help $match'
        await channel.send(help_list)

    if message.content.lower() == '$match':  # match commands
        help_list = \
            '$match: 오늘/다음 LCK 경기\n$match @@: 해당 팀의 다음 경기 (예: $match GEN/$match T1)'
        await channel.send(help_list)

    if message.content.lower() == '$match today':  # match today
        # fetch the next lck
        # TODO: 아직 LCK (하루 2경기) 시즌 중 게임만 지원함. 다른 게임 숫자도 지원하게 만들 것
        games = {schedule.raw_soup[0], schedule.raw_soup[1]}
        # league: league in which the game is in (i.e. lck)
        # teams: list of teams (will be 2x the game length)
        #
        league, teams, hours, ampmlist = [], [], [], []

        for game in games:  # iterate for each game
            for team in game.find_all('span', {"class": "tricode"}):  # add teams for each game
                teams.append(team.text)
            for hour in game.find_all('span', {"class": "hour"}):  # add teams for each game
                hours.append(hour.text)
            for ampm in game.find_all('span', {"class": "ampm"}):  # add teams for each game
                ampmlist.append(ampm.text)
            for leagueElem in game.find_all('div', {"class": "name"}):
                league.append(leagueElem.text)

        print('games:', games)
        print('teams: ', teams)
        print('hours: ', hours)
        print('ampm: ', ampmlist)
        print('league: ', league)

        response = ''
        for i in range(0, len(games)):
            response = (league[i] + ' ' + str(i+1) + '경기: ' + teams[(2*i)] + ' vs ' + teams[(2*i)+1]
                        + ', ' + ampmlist[i] + ' ' + hours[i] + '시')
            await channel.send(response)

    # ------- for debugging: prints all messages --------- #
    # if not message.author.bot: # do only if message is sent from user && is testMode
    #     print('message: ', message)
    #     print('message type: ', type(message.content))
    #     print('message content: ', message.content)

client.run(myToken)
