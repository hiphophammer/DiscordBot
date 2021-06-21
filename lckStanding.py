from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os
import numpy as np
import pandas as pd
import re


class LckStanding:
    url = 'https://lolesports.com/standings/lck/lck_summer_2021/regular_season'

    def __init__(self, url=url):
        # options for chromedriver
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=self.options)

        # set up variables for geoloc. overriding
        self.latitude = 37.206192
        self.longitude = 127.081014
        self.accuracy = 100

        # override geolocation
        self.wd.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy})

        self.wd.get(url)  # open url

        # press locale button
        self.locale_button = self.wd.find_element_by_class_name('lang-switch-trigger')
        self.wd.execute_script('arguments[0].click();', self.locale_button)

        # press 한국어 button
        try:
            self.kr_button = self.wd.find_element(By.LINK_TEXT, '한국어')
            self.wd.execute_script('arguments[0].click();', self.kr_button)
        except:  # if an exception occurs (= locale is already set to korean, just pass)
            pass

        self.html = self.wd.execute_script('return document.documentElement.outerHTML')
        self.soup = bs(self.html, 'html.parser')  # boil soup in Korean

        self.currentPointer = self.soup.find_all('a', class_=['ranking'])
        self.standing_cols = np.dtype([('team_name', str),
                                       ('ranking', str),  # league: i.e. 'lck'
                                       ('record', str)
                                       ])
        self.standing_data = np.empty(0, dtype=self.standing_cols)
        self.result_df = pd.DataFrame(self.standing_data)

        for row in self.currentPointer:
            temp_name = row.find('div', class_='name').text
            temp_ranking = row.find('div', class_=['ordinal', 'ordinal hidden']).text
            temp_record = row.find('div', class_='record').text
            temp_win, temp_loss = temp_record.split('-', 1)
            korean = re.compile('[\u3131-\u3163\uac00-\ud7a3]+')
            temp_win = re.sub(korean, '', temp_win)
            temp_loss = re.sub(korean, '', temp_loss)
            print(temp_name, temp_ranking, temp_record, temp_win, temp_loss)
            team_array = np.array([temp_name, temp_ranking, temp_record], dtype=str)
            df_temp = pd.DataFrame([team_array], columns=['team_name', 'ranking', 'record'])
            frames = [self.result_df, df_temp]
            self.result_df = pd.concat(frames, ignore_index=True)
