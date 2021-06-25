from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import os
import numpy as np
import pandas as pd
import re


# class instance for LCK Schedule
# has pandas dataframe for team1, team2, date
class LckSchedule:
    url = 'https://lolesports.com/schedule?leagues=lck'
    js = 'window._geoinfo = {"code":"KR","area":"AS","locale":"ko-KR"};' \
         'if ("serviceWorker" in navigator) ' \
         '{ navigator.serviceWorker.getRegistrations().then(function(registrations) ' \
         '{ for (var i = 0; i < registrations.length; i++) { registrations[i].unregister(); } ' \
         'if (window.location.href.indexOf("watch.lolesports.com/schedule") > -1)  ' \
         'window.location.replace("https://lolesports.com/schedule"); })}'

    # initializer
    def __init__(self, url=url):
        # options for chromedriver
        self.options = webdriver.ChromeOptions()
        self.options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        self.options.add_argument('headless')  # headless 모드 설정
        self.options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
        # self.options.add_argument("disable-gpu")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        # prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2,
        #                                                     'geolocation': 2, 'notifications': 2,
        #                                                     'auto_select_certificate': 2, 'fullscreen': 2,
        #                                                     'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
        #                                                     'media_stream_mic': 2, 'media_stream_camera': 2,
        #                                                     'protocol_handlers': 2, 'ppapi_broker': 2,
        #                                                     'automatic_downloads': 2, 'midi_sysex': 2,
        #                                                     'push_messaging': 2, 'ssl_cert_decisions': 2,
        #                                                     'metro_switch_to_desktop': 2,
        #                                                     'protected_media_identifier': 2, 'app_banner': 2,
        #                                                     'site_engagement': 2, 'durable_storage': 2}}
        # self.options.add_experimental_option('prefs', prefs)

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

        self.wd.execute_script(LckSchedule.js)
        self.html = self.wd.execute_script('return document.documentElement.outerHTML')
        self.soup = bs(self.html, 'html.parser')  # boil soup in Korean

        # current pointer for parsing
        self.currentPointer = self.soup.find_all('div',
                                                 class_=['divider live', 'divider future', 'EventDate', 'EventMatch'])

        self.past_cols = np.dtype([('date', str),
                                   ('league', str),  # league: i.e. 'lck'
                                   ('weekday', str),  # week of the day: i.e. 월요일/화요일
                                   ('first_team_tricode', str),  # first team: i.e. GEN
                                   ('first_team_score', str),
                                   ('second_team_tricode', str),
                                   ('second_team_score', str)
                                   ])
        self.live_cols = np.dtype([('date', str),
                                   ('league', str),  # league: i.e. 'lck'
                                   ('first_team_tricode', str),  # first team: i.e. GEN
                                   ('second_team_tricode', str),
                                   ('game_number', str)
                                   ])
        self.future_cols = np.dtype([('date', str),
                                     ('league', str),  # league: i.e. 'lck'
                                     ('weekday', str),  # week of the day: i.e. 월요일/화요일
                                     ('first_team_tricode', str),  # first team: i.e. GEN\
                                     ('second_team_tricode', str)
                                     ])

        self.past_data = np.empty(0, dtype=self.past_cols)
        self.live_data = np.empty(0, dtype=self.live_cols)
        self.future_data = np.empty(0, dtype=self.future_cols)

        self.result_df_past = pd.DataFrame(self.past_data)
        self.result_df_live = pd.DataFrame(self.live_data)
        self.result_df_future = pd.DataFrame(self.future_data)

        self.date_now = np.datetime64(datetime.datetime.now(), '[m]')
        self.date_string = ''
        self.current = 'past'
        self.match_weekday = ''
        print('Starting parsing...')
        for row in self.currentPointer:
            if self.current == 'past':  # past events
                if 'divider live' in str(row):  # divider live:
                    # delete the first row of result_array here:
                    self.current = 'current'
                    print('Past event done, switching to live event...', self.current)
                elif 'divider future' in str(row):
                    self.current = 'future'
                    print('No live event, switching to future event...', self.current)
                else:  # else: it's either EventDate or EventMatch
                    date = row.find('div', class_="date")  # see if can get date
                    if date != None:  # date isn't None (== date is valid); parse date from data
                        # get today's year
                        # TODO: this might not work at the end of the year
                        year_string = self.date_now.astype(str).split('-')[0]  # year in string i.e. 2001
                        monthday = row.find('span',
                                            {
                                                "class": "monthday"}).text  # string with month and day combined i.e. 6월 19일
                        month, day = re.findall('\d+', monthday)  # get month/day
                        if int(month) < 10:
                            month = '0' + month
                        if int(day) < 10:
                            day = '0' + day
                        self.date_string = year_string + '-' + month + '-' + day  # this will be combined to something like 2001-06-19
                        self.match_weekday = row.find('span', {"class": "weekday"}).text
                    else:  # date is None (== is an EventMatch)
                        # parse past match data
                        match_league = row.find('div', {"class": "name"}).text
                        first_team_name = row.find_all('span', {"class": "tricode"})[0].text
                        second_team_name = row.find_all('span', {"class": "tricode"})[1].text
                        first_team_score = int(row.find('span', {"class": "scoreTeam1"}).text)
                        second_team_score = int(row.find('span', {"class": "scoreTeam2"}).text)
                        hour = int(row.find('span', {"class": "hour"}).text)
                        if row.find('span', {"class": "ampm"}).text == '오후':  # if 오후, add 12 hours to the hour
                            hour += 12
                        hour = str(hour)
                        if int(hour) < 10:
                            hour = '0' + hour
                        match_date = (self.date_string + 'T' + hour)
                        match_array = np.array(
                            [str(match_date), match_league, self.match_weekday, first_team_name, first_team_score,
                             second_team_name, second_team_score], dtype=str)
                        df_temp = pd.DataFrame([match_array],
                                               columns=['date', 'league', 'weekday', 'first_team_tricode',
                                                        'first_team_score', 'second_team_tricode',
                                                        'second_team_score'])
                        # print(df_temp)
                        frames = [self.result_df_past, df_temp]
                        self.result_df_past = pd.concat(frames, ignore_index=True)
            elif self.current == 'current':  # current event(s): get only lck
                if 'divider future' in str(row):
                    self.current = 'future'
                    print('Live event done, switching to future events...', self.current)
                elif row.find('a', class_='single link live event lck') != None:  # live event is LCK
                    # getting info
                    self.date_string = str(np.datetime64(datetime.datetime.now(), '[h]'))
                    # match_league = row.find('div', {"class": "name"}).text
                    match_league = 'LCK'
                    first_team_name = row.find_all('span', {"class": "tricode"})[0].text
                    second_team_name = row.find_all('span', {"class": "tricode"})[1].text
                    # first_team_score = int(row.find('span', {"class": "scoreTeam1"}).text)
                    # second_team_score = int(row.find('span', {"class": "scoreTeam2"}).text)
                    game_number = re.findall('\d+', row.find('span', {"class": "game-number"}).text)[0]
                    match_array = np.array(
                        [str(self.date_string), match_league, first_team_name, second_team_name, game_number],
                        dtype=str)
                    df_temp = pd.DataFrame([match_array],
                                           columns=['date', 'league', 'first_team_tricode', 'second_team_tricode',
                                                    'game_number'])
                    frames = [self.result_df_live, df_temp]
                    self.result_df_live = pd.concat(frames, ignore_index=True)
            elif self.current == 'future':
                date = row.find('div', class_="date")
                if date != None:  # date isn't None (== date is valid); parse date from data
                    # get today's year
                    # TODO: this might not work at the end of the year
                    year_string = self.date_now.astype(str).split('-')[0]  # year in string i.e. 2001
                    monthday = row.find('span',
                                        {"class": "monthday"}).text  # string with month and day combined i.e. 6월 19일
                    month, day = re.findall('\d+', monthday)  # get month/day
                    if int(month) < 10:
                        month = '0' + month
                    if int(day) < 10:
                        day = '0' + day
                    self.date_string = year_string + '-' + month + '-' + day  # this will be combined to something like 2001-06-19
                    self.match_weekday = row.find('span', {"class": "weekday"}).text
                else:
                    # parse future match data
                    match_league = row.find('div', {"class": "name"}).text
                    first_team_name = row.find_all('span', {"class": "tricode"})[0].text
                    second_team_name = row.find_all('span', {"class": "tricode"})[1].text
                    hour = int(row.find('span', {"class": "hour"}).text)
                    if row.find('span', {"class": "ampm"}).text == '오후':  # if 오후, add 12 hours to the hour
                        hour += 12
                    hour = str(hour)
                    if int(hour) < 10:
                        hour = '0' + hour
                    match_date = (self.date_string + 'T' + hour)
                    match_array = np.array(
                        [str(match_date), match_league, self.match_weekday, first_team_name, second_team_name],
                        dtype=str)
                    df_temp = pd.DataFrame([match_array], columns=['date', 'league', 'weekday', 'first_team_tricode',
                                                                   'second_team_tricode'])
                    frames = [self.result_df_future, df_temp]
                    self.result_df_future = pd.concat(frames, ignore_index=True)
        print('Done creating base frames...')
        self.convert_dates()

    # convert all dates in all dataframes from numpy.str to pd.datetime
    def convert_dates(self):
        print('Converting all dates into pd.datetime...')
        # convert past dates
        for index, row in self.result_df_past.iterrows():  # convert numpy.str to str
            self.result_df_past['date'][index] = str(self.result_df_past['date'][index])
        self.result_df_past['date'] = pd.to_datetime(self.result_df_past['date'], format='%Y-%m-%dT%H')
        # convert live dates
        for index, row in self.result_df_live.iterrows():  # convert numpy.str to str
            self.result_df_live['date'][index] = str(self.result_df_live['date'][index])
        self.result_df_live['date'] = pd.to_datetime(self.result_df_live['date'], format='%Y-%m-%dT%H')
        # convert future dates
        for index, row in self.result_df_future.iterrows():  # convert numpy.str to str
            self.result_df_future['date'][index] = str(self.result_df_future['date'][index])
        self.result_df_future['date'] = pd.to_datetime(self.result_df_future['date'], format='%Y-%m-%dT%H')

    # refresh schedule
    def refresh(self):
        print('Refreshing...')
        self.wd.get(LckSchedule.url)  # open url

        # press locale button
        self.locale_button = self.wd.find_element_by_class_name('lang-switch-trigger')
        self.wd.execute_script('arguments[0].click();', self.locale_button)

        # press 한국어 button
        try:
            self.kr_button = self.wd.find_element(By.LINK_TEXT, '한국어')
            self.wd.execute_script('arguments[0].click();', self.kr_button)
        except:  # if an exception occurs (= locale is already set to korean, just pass)
            pass

        self.wd.execute_script(LckSchedule.js)
        self.html = self.wd.execute_script('return document.documentElement.outerHTML')
        self.soup = bs(self.html, 'html.parser')  # boil soup in Korean

        # current pointer for parsing
        self.currentPointer = self.soup.find_all('div',
                                                 class_=['divider live', 'divider future', 'EventDate', 'EventMatch'])

        self.past_cols = np.dtype([('date', str),
                                   ('league', str),  # league: i.e. 'lck'
                                   ('weekday', str),  # week of the day: i.e. 월요일/화요일
                                   ('first_team_tricode', str),  # first team: i.e. GEN
                                   ('first_team_score', str),
                                   ('second_team_tricode', str),
                                   ('second_team_score', str)
                                   ])
        self.live_cols = np.dtype([('date', str),
                                   ('league', str),  # league: i.e. 'lck'
                                   ('first_team_tricode', str),  # first team: i.e. GEN
                                   ('second_team_tricode', str),
                                   ('game_number', str)
                                   ])
        self.future_cols = np.dtype([('date', str),
                                     ('league', str),  # league: i.e. 'lck'
                                     ('weekday', str),  # week of the day: i.e. 월요일/화요일
                                     ('first_team_tricode', str),  # first team: i.e. GEN\
                                     ('second_team_tricode', str)
                                     ])

        self.past_data = np.empty(0, dtype=self.past_cols)
        self.live_data = np.empty(0, dtype=self.live_cols)
        self.future_data = np.empty(0, dtype=self.future_cols)

        self.result_df_past = pd.DataFrame(self.past_data)
        self.result_df_live = pd.DataFrame(self.live_data)
        self.result_df_future = pd.DataFrame(self.future_data)

        self.date_now = np.datetime64(datetime.datetime.now(), '[m]')
        self.date_string = ''
        self.current = 'past'
        self.match_weekday = ''
        print('Starting parsing...')
        for row in self.currentPointer:
            if self.current == 'past':  # past events
                if 'divider live' in str(row):  # divider live:
                    # delete the first row of result_array here:
                    self.current = 'current'
                    print('Past event done, switching to live event...', self.current)
                elif 'divider future' in str(row):
                    self.current = 'future'
                    print('No live event, switching to future event...', self.current)
                else:  # else: it's either EventDate or EventMatch
                    date = row.find('div', class_="date")  # see if can get date
                    if date != None:  # date isn't None (== date is valid); parse date from data
                        # get today's year
                        # TODO: this might not work at the end of the year
                        year_string = self.date_now.astype(str).split('-')[0]  # year in string i.e. 2001
                        monthday = row.find('span',
                                            {
                                                "class": "monthday"}).text  # string with month and day combined i.e. 6월 19일
                        month, day = re.findall('\d+', monthday)  # get month/day
                        if int(month) < 10:
                            month = '0' + month
                        if int(day) < 10:
                            day = '0' + day
                        self.date_string = year_string + '-' + month + '-' + day  # this will be combined to something like 2001-06-19
                        self.match_weekday = row.find('span', {"class": "weekday"}).text
                    else:  # date is None (== is an EventMatch)
                        # parse past match data
                        match_league = row.find('div', {"class": "name"}).text
                        first_team_name = row.find_all('span', {"class": "tricode"})[0].text
                        second_team_name = row.find_all('span', {"class": "tricode"})[1].text
                        first_team_score = int(row.find('span', {"class": "scoreTeam1"}).text)
                        second_team_score = int(row.find('span', {"class": "scoreTeam2"}).text)
                        hour = int(row.find('span', {"class": "hour"}).text)
                        if row.find('span', {"class": "ampm"}).text == '오후':  # if 오후, add 12 hours to the hour
                            hour += 12
                        hour = str(hour)
                        if int(hour) < 10:
                            hour = '0' + hour
                        match_date = (self.date_string + 'T' + hour)
                        match_array = np.array(
                            [str(match_date), match_league, self.match_weekday, first_team_name, first_team_score,
                             second_team_name, second_team_score], dtype=str)
                        df_temp = pd.DataFrame([match_array],
                                               columns=['date', 'league', 'weekday', 'first_team_tricode',
                                                        'first_team_score', 'second_team_tricode',
                                                        'second_team_score'])
                        # print(df_temp)
                        frames = [self.result_df_past, df_temp]
                        self.result_df_past = pd.concat(frames, ignore_index=True)
            elif self.current == 'current':  # current event(s): get only lck
                if 'divider future' in str(row):
                    self.current = 'future'
                    print('Live event done, switching to future events...', self.current)
                elif row.find('a', class_='single link live event lck') != None:  # live event is LCK
                    # getting info
                    self.date_string = str(np.datetime64(datetime.datetime.now(), '[h]'))
                    # match_league = row.find('div', {"class": "name"}).text
                    match_league = 'LCK'
                    first_team_name = row.find_all('span', {"class": "tricode"})[0].text
                    second_team_name = row.find_all('span', {"class": "tricode"})[1].text
                    # first_team_score = int(row.find('span', {"class": "scoreTeam1"}).text)
                    # second_team_score = int(row.find('span', {"class": "scoreTeam2"}).text)
                    game_number = re.findall('\d+', row.find('span', {"class": "game-number"}).text)[0]
                    match_array = np.array(
                        [str(self.date_string), match_league, first_team_name, second_team_name, game_number],
                        dtype=str)
                    df_temp = pd.DataFrame([match_array],
                                           columns=['date', 'league', 'first_team_tricode', 'second_team_tricode',
                                                    'game_number'])
                    frames = [self.result_df_live, df_temp]
                    self.result_df_live = pd.concat(frames, ignore_index=True)
            elif self.current == 'future':
                date = row.find('div', class_="date")
                if date != None:  # date isn't None (== date is valid); parse date from data
                    # get today's year
                    # TODO: this might not work at the end of the year
                    year_string = self.date_now.astype(str).split('-')[0]  # year in string i.e. 2001
                    monthday = row.find('span',
                                        {"class": "monthday"}).text  # string with month and day combined i.e. 6월 19일
                    month, day = re.findall('\d+', monthday)  # get month/day
                    if int(month) < 10:
                        month = '0' + month
                    if int(day) < 10:
                        day = '0' + day
                    self.date_string = year_string + '-' + month + '-' + day  # this will be combined to something like 2001-06-19
                    self.match_weekday = row.find('span', {"class": "weekday"}).text
                else:
                    # parse future match data
                    match_league = row.find('div', {"class": "name"}).text
                    first_team_name = row.find_all('span', {"class": "tricode"})[0].text
                    second_team_name = row.find_all('span', {"class": "tricode"})[1].text
                    hour = int(row.find('span', {"class": "hour"}).text)
                    if row.find('span', {"class": "ampm"}).text == '오후':  # if 오후, add 12 hours to the hour
                        hour += 12
                    hour = str(hour)
                    if int(hour) < 10:
                        hour = '0' + hour
                    match_date = (self.date_string + 'T' + hour)
                    match_array = np.array(
                        [str(match_date), match_league, self.match_weekday, first_team_name, second_team_name],
                        dtype=str)
                    df_temp = pd.DataFrame([match_array], columns=['date', 'league', 'weekday', 'first_team_tricode',
                                                                   'second_team_tricode'])
                    frames = [self.result_df_future, df_temp]
                    self.result_df_future = pd.concat(frames, ignore_index=True)
        print('Done creating base frames...')
        self.convert_dates()

    def search_for_next_match(self, team_code):
        target_index = 0
        target_found = False
        for index, row in self.result_df_future.iterrows():
            if (row['first_team_tricode'] == team_code or row['second_team_tricode'] == team_code) and \
                    target_found is False:
                target_index = index
                target_found = True
            if target_found is True:
                break
        return self.result_df_future[target_index:target_index+1], target_index

    def get_last_match(self):
        self.refresh()
        return self.result_df_past[len(self.result_df_past)-1:len(self.result_df_past)], len(self.result_df_past)-1

    def get_next_match(self):
        # start from today
        closest_day = self.result_df_future['date'][0] # get date of the first future match
        # TODO: idk if it'll work when there's no future match.
        stop_index = 0
        # repeat until day is found
        while self.is_the_same_date(closest_day, self.result_df_future['date'][stop_index+1]):
            stop_index += 1
        return self.result_df_future[0:stop_index+1]

    @staticmethod
    def is_the_same_date(date1, date2):
        print('Comparing ', str(date1), ' and ', str(date2), '...')
        if date1.year == date2.year and date1.month == date2.month and date1.day == date2.day:
            return True
        else:
            return False

    def get_todays_matches(self):
        self.refresh()
        print('--- done refreshing, getting today\'s schedule...')
        # today game
        today_date = pd.to_datetime(np.datetime64(datetime.datetime.now(), '[m]'), format='%Y-%m-%dT%H')
        # today_date = pd.to_datetime(np.datetime64('2021-06-20T18', '[m]'), format='%Y-%m-%dT%H')
        print('today date: ', today_date)

        # past game
        lowest_past_game_index = len(self.result_df_past) - 1
        if self.is_the_same_date(today_date, self.result_df_past['date'][lowest_past_game_index]):
            lowest_past_game_index -= 1
            while self.is_the_same_date(today_date, self.result_df_past['date'][lowest_past_game_index]):
                lowest_past_game_index -= 1

        # future game
        print('--- getting future games...---')

        highest_future_game_index = 0

        if self.is_the_same_date(today_date, self.result_df_future['date'][highest_future_game_index]):
            highest_future_game_index += 1
            while self.is_the_same_date(today_date, self.result_df_future['date'][highest_future_game_index]):
                highest_future_game_index += 1
        # end of getting indices; slice dataframes

        print('Done!')
        print('Lowest index: ', lowest_past_game_index)
        print('Highest index: ', highest_future_game_index)

        # try:
        #     today_past_df = self.result_df_past[lowest_past_game_index:len(self.result_df_past)]
        # except:
        today_past_df = self.result_df_past[0:0]
        try:
            today_future_df = self.result_df_future[0:highest_future_game_index]
        except:
            print('today_future_df exception!')
            today_future_df = self.result_df_future[0:0]
        return today_past_df, self.result_df_live, today_future_df
