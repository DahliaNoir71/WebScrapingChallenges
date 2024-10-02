import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

BASE_URL = 'http://quotes.toscrape.com/'
USERNAME = 'DahliaNoir'
PASSWORD = 'python'
URL_SCROLL = 'http://quotes.toscrape.com/scroll'
SCROLL_PAUSE_TIME = 0.5
URL_FIRST_QUOTE = 'https://quotes.toscrape.com/js/page/10/'


def fetch_page(url):
    """Fetch page content with given URL using HTTP authentication."""
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    return BeautifulSoup(response.text, 'html.parser')


def count_pages():
    """Count the number of paginated pages starting from BASE_URL."""
    nb_pages = 1
    current_url = BASE_URL
    while True:
        soup = fetch_page(current_url)
        li_next = soup.find('li', class_='next')
        if li_next:
            next_page_url = li_next.find('a')['href']
            current_url = BASE_URL + next_page_url
            nb_pages += 1
        else:
            break
    print(f'Number of pages: {nb_pages}')


def count_quotations():
    """Scroll through the URL_SCROLL page and count the number of quotes."""
    browser = webdriver.Firefox()
    browser.get(URL_SCROLL)
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    nb_quotes = len(browser.find_elements(By.CLASS_NAME, value='quote'))
    browser.close()
    print(f'Number of quotations: {nb_quotes}')


def print_first_quote():
    """Fetch and print the first quote from URL_FIRST_QUOTE."""
    soup = fetch_page(URL_FIRST_QUOTE)
    div_quotes = soup.find_all('div', class_='quote')
    print(div_quotes)


count_pages()
count_quotations()
print_first_quote()
