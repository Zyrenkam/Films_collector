from selenium import webdriver
from selenium.webdriver.support.select import By
from pathlib import Path
import os


def get_film(url):
    print('Downloading film!')

    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.get(url)

    # get info about film
    name = browser.find_element(By.XPATH, '//*[@id="dle-content"]/div[2]/div[1]/h1').text
    year = browser.find_element(By.XPATH, '//*[@id="dle-content"]/article/div[2]/div[2]/span').text
    description = browser.find_element(By.XPATH, '//*[@id="dle-content"]/div[7]/div[1]/p[2]').text
    genre = browser.find_element(By.XPATH, '//*[@id="dle-content"]/div[12]').text.split(':')[1]

    # download video
    button = browser.find_element(By.XPATH, '//*[@id="dle-content"]/div[9]/div[2]/a')

    # //*[@id="dle-content"]/div[9]/div[2]/a  320x240 low
    # //*[@id="dle-content"]/div[9]/div[3]/a  720x304 high

    button.click()
    browser.close()

    # change film's path
    cur_path = os.getcwd()

    downloads_path = str(Path.home() / "Downloads")
    files = os.listdir(downloads_path)

    for i in range(0, len(files)):
        if '.mp4' in files[i]:
            os.rename(str(downloads_path + '\\' + files[i]), str(cur_path + '\\' + name.replace(' ', '_') + '.mp4'))

    print('Video was downloaded')

    return name, description, year, genre
