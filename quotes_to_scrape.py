import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs

BASE_URL = 'http://quotes.toscrape.com/'
USERNAME = 'DahliaNoir'
PASSWORD = 'python'



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

get_nb_pages()