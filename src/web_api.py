import requests
from bs4 import BeautifulSoup


def get_books():

    url = "https://books.toscrape.com/"

    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.select("article.product_pod")

    result = []

    for book in books:

        name = book.h3.a["title"]

        price = book.select_one(
            ".price_color"
        ).text

        result.append({
            "name": name,
            "price": price
        })

    return result