import lckSchedule as ls

schedule = ls.LckSchedule()

# TODO: 아직 LCK (하루 2경기) 시즌 중 게임만 지원함. 다른 게임 숫자도 지원하게 만들 것
games = {schedule.raw_soup[0], schedule.raw_soup[1]}
league = []
teams = []
hours = []
ampmlist = []

for game in games: # iterate for each game
    for team in game.find_all('span', {"class": "tricode"}): # add teams for each game
        teams.append(team.text)
    for hour in game.find_all('span', {"class": "hour"}): # add teams for each game
        hours.append(hour.text)
    for ampm in game.find_all('span', {"class": "ampm"}): # add teams for each game
        ampmlist.append(ampm.text)
    for leagueElem in game.find_all('div', {"class": "name"}):
        league.append(leagueElem.text)

print('games:', games)
print('teams: ', teams)
print('hours: ', hours)
print('ampm: ', ampmlist)
print('league: ', league)

for i in range(0, len(games)):
    print(i+1, '경기: ', teams[(2*i)], ' vs ', teams[(2*i)+1],
          ', ', ampmlist[i], ' ', hours[i], '시')

# print(teams)
# print('1경기: ', teams[0], ' vs ', teams[1])
# print('')