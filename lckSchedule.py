from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By


# class instance for LCK Schedule
# has pandas dataframe for team1, team2, date
class LckSchedule:
    url = 'https://lolesports.com/schedule?leagues=lck'

    # initializer
    def __init__(self, url=url):
        # set up chromedriver
        self.driver = webdriver.Chrome(executable_path="/app/.chromedriver/bin/chromedriver/chromedriver.exe")

        # options for chromedriver
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_experimental_option('prefs', {'intl.accept_languages': 'ko,ko_KR'})
        self.wd = webdriver.Chrome('chromedriver', options=self.options)

        # set up variables for geoloc. overriding
        self.latitude = 37.206192
        self.longitude = 127.081014
        self.accuracy = 100

        # override geolocation
        self.wd.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy})

        self.wd.get(url) # open url

        js = 'window._geoinfo = {"code":"KR","area":"AS","locale":"ko-KR"};if ("serviceWorker" in navigator) { navigator.serviceWorker.getRegistrations().then(function(registrations) { for (var i = 0; i < registrations.length; i++) { registrations[i].unregister(); } if (window.location.href.indexOf("watch.lolesports.com/schedule") > -1)  window.location.replace("https://lolesports.com/schedule"); })}'
        # press locale button
        self.locale_button = self.wd.find_element_by_class_name('lang-switch-trigger')
        self.wd.execute_script('arguments[0].click();', self.locale_button)

        # press 한국어 button
        try:
            self.kr_button = self.wd.find_element(By.LINK_TEXT, '한국어')
            self.wd.execute_script('arguments[0].click();', self.kr_button)
        except: # if an exception occurs (= locale is already set to korean, just pass)
            pass

        self.wd.execute_script(js)
        self.html = self.wd.execute_script('return document.documentElement.outerHTML')
        self.soup = bs(self.html, 'html.parser') # boil soup in Korean

        # testing block: print out geoinfo from javascript file
        # self.element = self.wd.execute_script("return window._geoinfo")
        # print(self.element)

        self.raw_soup = self.soup.findAll('div', class_='single future event')
        for row in self.raw_soup:
            print(row)

    # returns next schedule in pd
    def get_next(self):
        return self.raw_soup[0]

    # returns the whole schedule in pd


lck = LckSchedule()