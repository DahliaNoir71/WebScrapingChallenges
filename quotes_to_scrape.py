import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = 'http://quotes.toscrape.com/'
USERNAME = 'DahliaNoir'
PASSWORD = 'python'
URL_SCROLL = 'http://quotes.toscrape.com/scroll'
SCROLL_PAUSE_TIME = 0.5


def get_nb_pages():
    #global base_url, username, password
    nb_pages = 1
    current_url = BASE_URL
    while True:
        response = requests.get(current_url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        soup = bs(response.text, 'html.parser')
        li_next = soup.find('li', class_='next')
        if li_next:
            next_page_url = li_next.find('a')['href']
            current_url = BASE_URL + next_page_url
            nb_pages += 1
        else:
            break

    print('Nb pages : ' + str(nb_pages))

def get_nb_quotations():
    nb_quotes = 0
    browser = webdriver.Firefox()
    browser.get(URL_SCROLL)


    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    nb_quotes = len(browser.find_elements(By.CLASS_NAME, value='quote'))
    browser.close()

    print('Nb quotations : ' + str(nb_quotes))


get_nb_pages()

get_nb_quotations()