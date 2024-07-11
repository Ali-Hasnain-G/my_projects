from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)

#   scrape_engoo(): Scrapes the Engoo website and saves the data to `output.csv`. It returns the data as a dictionary.

def scrape_engoo():
    url = 'https://engoo.com/'
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    links = soup.find_all('a')
    
    data = {
        'Link Text': [link.text for link in links],
        'URL': [link.get('href') for link in links]
    }
    df = pd.DataFrame(data)
    df.to_csv('output.csv', index=False)
    
    return data

# scrape_books(): Scrapes the Books to Scrape website and saves the data to `books.csv`. It returns the data as a dictionary.

def scrape_books():
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
    
    return data

# /scrape/engoo: Calls `scrape_engoo()` when accessed via a GET request and returns the scraped data as JSON.

@app.route('/scrape/engoo', methods=['GET'])
def scrape_engoo_route():
    data = scrape_engoo()
    return jsonify(data)

# /scrape/books: Calls `scrape_books()` when accessed via a GET request and returns the scraped data as JSON.

@app.route('/scrape/books', methods=['GET'])
def scrape_books_route():
    data = scrape_books()
    return jsonify(data)

# Running the Flask App:
# The Flask app runs in debug mode, listening for requests. When a request is made to one of the defined routes, the corresponding scraping function is called, and the scraped data is returned as a JSON response.


if __name__ == '__main__':
    app.run(debug=True)