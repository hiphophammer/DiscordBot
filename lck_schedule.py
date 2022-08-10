from selenium.webdriver.common.by import By
from dataclasses import dataclass
from datetime import datetime
import selenium_utility as SU


@dataclass()
class Match:
    match_time: datetime = None
    match_day_of_week: str = None
    number_of_games: int = None
    home_team: str = None
    away_team: str = None
    home_score: int = None
    away_score: int = None


class LckSchedule:
    url = 'https://game.naver.com/esports/schedule/lck'
    matches = []

    def __refresh(self):
        wd = self.wd
        # open webpage and wait for the page to load
        wd.get(self.url)
        SU.wait_for_element(wd, By.XPATH, './/div[contains(@class, "schedule_calendar_select_date__2a2Rf")]')
        year = int(wd.find_element(By.CLASS_NAME, 'schedule_calendar_txt_year__hT9Ws').text)
        game_days_raw = wd.find_elements(By.CLASS_NAME, 'card_item__3Covz')
        for game_day in game_days_raw:
            date_raw = game_day.find_element(By.CLASS_NAME, 'card_date__1kdC3').text
            month = int(date_raw[0:2])
            day = int(date_raw[4:6])
            day_of_week = date_raw[9:10]
            matches_raw = game_day.find_elements(By.CLASS_NAME, 'row_item__dbJjy')
            for match_raw in matches_raw:
                match = Match()
                self.matches.append(match)

    def refresh(self):
        self.wd.refresh()
        self.__refresh()

    def __init__(self):
        # initiate webdriver
        self.wd = SU.setup_webdriver()
        wd = self.wd
        wd.get(self.url)

        # refresh() to get the standing info
        self.__refresh()
