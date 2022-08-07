from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')  # headless 모드 설정
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("window-size=1920x1080")  # 화면크기(전체화면)
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    prefs = {'profile.default_content_setting_values': {'plugins': 2,
                                                        'geolocation': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                        'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2,
                                                        'ppapi_broker': 2,
                                                        'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement': 2}}
    #
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# if there's any alert popup, attempt to close it
def close_alert(wd):
    try:
        wd.switch_to.alert.accept()
        return
    except:
        return


def wait_for_element(wd, elem_by, description, time=10):
    try:
        elem = wd.find_element(elem_by, description)
        return elem
    except:
        dummy = WebDriverWait(wd, time).until(EC.presence_of_element_located((elem_by, description)))
        elem = wd.find_element(elem_by, description)
        return elem
