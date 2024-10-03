import requests
from bs4 import BeautifulSoup

# Constantes
URL_BOOKS = 'https://books.toscrape.com/'
STATUS_OK = 200
BOOKS_PER_PAGE = 20
URL_PREFIX = URL_BOOKS + 'catalogue/category/books/'
TO_REMOVE_CATEGORY = 'Books'


def get_response(url):
    """
    :param url: The URL to which the GET request is to be sent.
    :return: The response object resulting from the GET request to the specified URL.
    """
    return requests.get(url)


def get_soup(response):
    """
    :param response: The HTTP response object containing the HTML content.
    :return: A BeautifulSoup object initialized with the HTML content from the response.
    """
    return BeautifulSoup(response.text, 'html.parser')


def extract_categories():
    """
    Extracts categories from a books website and returns them as a list of dictionaries.
    Each dictionary contains the 'name' of the category and the 'url_first_page' of the corresponding category page.

    :return: A list of dictionaries, where each dictionary contains 'name' and 'url_first_page' keys.
    """
    response = get_response(URL_BOOKS)
    if response.status_code != STATUS_OK:
        print("Non connecté à la page d'accueil")
        return []

    soup = get_soup(response)
    ul_nav = soup.find('ul', class_='nav-list')
    li_nav = ul_nav.find('li')
    a_categories = li_nav.find_all('a')
    categories = []

    for a_category in a_categories:
        category_text = a_category.get_text().strip()
        if category_text != TO_REMOVE_CATEGORY:
            categories.append({
                'name': category_text,
                'url_first_page': a_category['href']
            })

    return categories


def compute_category_details(category):
    """
    :param category: Dictionary containing information about a book category. It should contain at least a key 'url_first_page' which points to the first page of the category's book listings.
    :return: None. The function updates the input category dictionary in place with additional details including number of books ('nb_books'), number of pages ('nb_pages'), total price of all books ('total_price'), and average book price ('average_price').
    """
    url_category = URL_BOOKS + category['url_first_page']
    response = get_response(url_category)
    if response.status_code != STATUS_OK:
        return

    soup = get_soup(response)
    form = soup.find('form', class_='form-horizontal')
    nb_books = int(form.find('strong').get_text().strip())
    nb_pages = nb_books // BOOKS_PER_PAGE + (1 if nb_books % BOOKS_PER_PAGE != 0 else 0)
    pages_url = [url_category] + [url_category.replace('index.html', f'page-{x}.html') for x in range(2, nb_pages + 1)]

    total_price = 0
    for page_url in pages_url:
        response = get_response(page_url)
        if response.status_code == STATUS_OK:
            p_prices = soup.find_all('p', class_='price_color')
            for p_price in p_prices:
                price = float(p_price.get_text().strip()[2:])
                total_price += price

    category.update({
        'nb_books': nb_books,
        'nb_pages': nb_pages,
        'total_price': round(total_price, 2),
        'average_price': round(total_price / nb_books, 2)
    })


def print_category_details(categories):
    """
    :param categories: List of category dictionaries. Each dictionary contains details of a specific category such as name, number of books, and average price.
    :return: None
    """
    for category in categories:
        compute_category_details(category)
        print(f"Category: {category['name']} - nb Books: {category['nb_books']} - "
              f"Average price: {category['average_price']}")


def main():
    """
    Extracts categories and prints their details.

    :return: None
    """
    categories = extract_categories()
    if categories:
        print_category_details(categories)


if __name__ == '__main__':
    main()
