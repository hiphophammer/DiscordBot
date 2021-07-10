import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import time

start_time = time.time()

# session = HTMLSession()
# r = session.get('https://hangang.ivlis.kr/')
# r.html.render()
# soup = BeautifulSoup(r.text, 'html.parser')


contents = requests.get('https://hangang.ivlis.kr/aapi.php?type=dgr')
soup = BeautifulSoup(contents.text, 'html.parser')


print(contents.text)
print("--- %s 초 경과 ---" % (time.time() - start_time))
