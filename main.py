# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import selenium
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import mutagen
import requests


def init(driver, country, decade):
    driver.get("https://radiooooo.com")
    driver.implicitly_wait(3)
    button_divs = driver.find_elements(by=By.CLASS_NAME, value='action')
    in_button = button_divs[1].find_elements(By.TAG_NAME, 'button')[0]
    in_button.click()
    driver.implicitly_wait(3)
    country_button = driver.find_element(By.CSS_SELECTOR, '.view.station.show')
    country_button.click()
    country_list = driver.find_element(By.XPATH, '/html/body/div[2]/div[10]/div/div[2]')
    for item in country_list.find_elements(By.CSS_SELECTOR, '*'):
        if item.text == country:
            item.click()
            break
    for item in driver.find_elements(By.CLASS_NAME, 'decade'):
        if item.text == decade:
            item.click()
            break

def extract_data(driver, player, info):
    #first setup the elements
    print(player)
    url = (player.find_element(By.CLASS_NAME, 'audio').find_elements(By.TAG_NAME, 'source')[1].get_attribute('src'))
    artist = (info.find_element(By.CLASS_NAME, 'artist').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
    title = (info.find_element(By.CLASS_NAME, 'title').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
    country = (info.find_element(By.CLASS_NAME, 'country').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
    year = (info.find_element(By.CLASS_NAME, 'country').find_elements(By.CLASS_NAME, 'text')[3].get_attribute('innerHTML'))
    author = (info.find_element(By.CLASS_NAME, 'author').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
    label = (info.find_element(By.CSS_SELECTOR, '.field.label').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
    audio = requests.get(url)
    input()
    fname = f'{artist} - {title}.ogg'.replace('/','-')
    print(fname)
    with open(fname, 'wb') as f:
        f.write(audio.content)
    file = mutagen.File(fname)
    file["artist"] = artist
    file["title"] = title
    file["country"] = country
    file["year"] = year
    file["author"] = author
    file["label"] = label
    file.pprint()
    file.save()
    wait = WebDriverWait(info, timeout=300)
    while True:
        wait.until((lambda inf : inf.find_element(By.CLASS_NAME, 'title').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML') != title))
        info = driver.find_element(By.CSS_SELECTOR, '.info.track')
        player = driver.find_element(By.CLASS_NAME,'audio-player')
        url = (player.find_element(By.CLASS_NAME, 'audio').find_elements(By.TAG_NAME, 'source')[1].get_attribute('src'))
        artist = (info.find_element(By.CLASS_NAME, 'artist').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
        title = (info.find_element(By.CLASS_NAME, 'title').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
        country = (info.find_element(By.CLASS_NAME, 'country').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
        year = (info.find_element(By.CLASS_NAME, 'country').find_elements(By.CLASS_NAME, 'text')[3].get_attribute('innerHTML'))
        author = (info.find_element(By.CLASS_NAME, 'author').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
        label = (info.find_element(By.CSS_SELECTOR, '.field.label').find_elements(By.CLASS_NAME, 'text')[1].get_attribute('innerHTML'))
        audio = requests.get(url)
        print(url)
        fname = f'{artist} - {title}.ogg'.replace('/','-')
        print(fname)
        with open(fname, 'wb') as f:
            f.write(audio.content)
        file = mutagen.File(fname)
        file["artist"] = artist
        file["title"] = title
        file["country"] = country
        file["year"] = year
        file["author"] = author
        file["label"] = label
        file.save()


if __name__ == '__main__':
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    init(driver, 'China', '1960')
    driver.implicitly_wait(3)
    driver.maximize_window()
    #expand the player
    info = driver.find_element(By.CSS_SELECTOR, '.info.track')
    player = driver.find_element(By.CLASS_NAME,'audio-player')
    extract_data(driver, player, info)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

