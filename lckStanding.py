from selenium.webdriver.common.by import By
from dataclasses import dataclass

import selenium_utility as SU


@dataclass
class Team:
    name: str = None
    rank: int = None
    wins: int = None
    losses: int = None
    difference: int = None


class LckStanding:
    url = 'https://game.naver.com/esports/record/lck/team/lck_2022_summer'
    teams = []

    def refresh(self, wd):
        # open webpage and wait for the page to load
        wd.get(self.url)
        SU.wait_for_element(wd, By.XPATH, '//*[@id="civ"]/div/div/div/div/div[2]/div[1]/ul/li[1]')
        team_names = wd.find_elements(By.CLASS_NAME, 'record_list_name__27huQ')

        wrapper = wd.find_element(By.CLASS_NAME, 'record_list_wrap_filter__1Ux0E')
        stats = wrapper.find_elements(By.CLASS_NAME, 'record_list_item__2fFsp')
        # update team stats from #1 to #10
        for i in range(10):
            team_stats = stats[i].find_elements(By.CLASS_NAME, 'record_list_data__3wyY7')

            self.teams[i].rank = i+1
            self.teams[i].name = team_names[i].text
            self.teams[i].wins = int(team_stats[0].text)
            self.teams[i].losses = int(team_stats[1].text)
            self.teams[i].difference = int(team_stats[2].text)

    def __print_standing(self):
        for team in self.teams:
            print(f'{team.rank}위 {team.name} / {team.wins}승 {team.losses}패 / 득실 {team.difference}')

    def __init__(self, url=url):
        # initialize list
        for s in range(10):
            self.teams.append(Team())

        # initiate webdriver
        self.wd = SU.setup_webdriver()
        wd = self.wd
        wd.get(url)

        # refresh() to get the standing info
        self.refresh(wd)
