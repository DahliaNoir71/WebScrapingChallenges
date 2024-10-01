import requests as req
from bs4 import BeautifulSoup as bs

url_books = 'https://books.toscrape.com/'
status_ok = 200
nb_books_per_page = 20
url_prefix = url_books + 'catalogue/category/books/'

categories = []
response = req.get(url_books)
if response.status_code == status_ok:
    to_remove = 'Books'
    soup = bs(response.text, 'html.parser')
    ul_nav = soup.find('ul', class_='nav-list')
    li_nav = ul_nav.find('li')
    a_categories = li_nav.find_all('a')
    for a_category in a_categories:
        category_text = a_category.get_text().strip()
        if category_text != to_remove:
            category = {
                    'name': category_text,
                    'url_first_page': a_category['href']
            }
            categories.append(category)
            url_category = url_books + category['url_first_page']
            response = req.get(url_category)
            if response.status_code == status_ok:
                soup = bs(response.text, 'html.parser')
                form = soup.find('form', class_='form-horizontal')
                nb_books = int(form.find('strong').get_text().strip())
                pages_url = [url_category]
                page_url_prefix = url_category.replace('index.html', '')
                if nb_books >= nb_books_per_page:
                    nb_pages = nb_books // nb_books_per_page + 1
                else:
                    nb_pages = 1
                if nb_pages > 1:
                    for x in range(2, nb_pages):
                        pages_url.append(page_url_prefix + 'page-' + str(x) + '.html')
                category['nb_books'] = int(nb_books)
                category['nb_pages'] = int(nb_pages)
                total_price = 0
                for page_url in pages_url:
                    response = req.get(page_url)
                    if response.status_code == status_ok:
                        p_prices = soup.find_all('p', class_='price_color')
                        for p_price in p_prices:
                            price = p_price.get_text().strip()[2:]
                            total_price += float(price)
                average_price = total_price / nb_books
                category['total_price'] = round(total_price, 2)
                category['average_price'] = round(average_price, 2)
                print(
                    'Category:' + category['name']
                    + ' - nb Books: ' + str(category['nb_books'])
                    + ' - nb Pages:' + str(category['nb_pages'])
                    + ' - Total price:' + str(category['total_price'])
                    + ' - Average price:' + str(category['average_price'])
                )



else:
    print("Non connecté à la page d'accueil")





