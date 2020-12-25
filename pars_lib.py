import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"


def open_browser():
    global user_agent

    option = Options()
    option.add_argument("--no-sandbox")
    option.add_argument("start-maximized")
    
    # Pass the argument 1 to allow and 2 to block
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.stylesheets": 1,
        "profile.managed_default_content_settings.cookies": 1,
        "profile.managed_default_content_settings.javascript": 1,
        "profile.managed_default_content_settings.plugins": 1,
        "profile.managed_default_content_settings.popups": 2,
        "profile.managed_default_content_settings.geolocation": 2,
        "profile.managed_default_content_settings.media_stream": 1,
    }
    option.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=option, executable_path='/Users/user/Desktop/chromedriver')
    return browser


def scroll_and_load(driver, load_time=0):
    # Get scroll height
    page_height = driver.execute_script("return document.body.scrollHeight")
    current_scroll = 0
    while current_scroll <= page_height:
        # Scroll 350 pix down
        driver.execute_script("window.scrollTo(0, " + str(current_scroll) + ");")
        time.sleep(random.randint(0, load_time))
        current_scroll += 350


def get_html(url, browser=None, load_time=None):
    if browser is None:
        return requests.get(url).text
    elif load_time is None:
        browser.get(url)
        time.sleep(random.randint(2, 5))
        return browser.page_source
    else:
        browser.get(url)
        scroll_and_load(browser, load_time)
        return browser.page_source


def close_browser(browser):
    browser.quit()
