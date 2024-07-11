import requests

url = 'http://example.com'
response = requests.get(url)
html_content = response.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')

# Example: Extract all the links from the webpage
links = soup.find_all('a')
for link in links:
    print(link.get('href'))

import pandas as pd

data = {
    'Link Text': [link.text for link in links],
    'URL': [link.get('href') for link in links]
}
df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://books.toscrape.com/catalogue/page-1.html'
base_url = 'http://books.toscrape.com/catalogue/'
book_titles = []
book_prices = []

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = soup.find_all('article', class_='product_pod')
    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        book_titles.append(title)
        book_prices.append(price)

    next_button = soup.find('li', class_='next')
    if next_button:
        next_page = next_button.a['href']
        url = base_url + next_page
    else:
        break

data = {
    'Title': book_titles,
    'Price': book_prices
}
df = pd.DataFrame(data)
df.to_csv('books.csv', index=False)

print("Scraping completed. Data saved to 'books.csv'.")
