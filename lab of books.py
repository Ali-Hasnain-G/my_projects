from flask import Flask, jsonify, request
import pandas as pd
app = Flask(__name__)

# Sample data (in real-world scenario, you would fetch data from a database)
my_books = pd.read_csv('')

# Endpoint to get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(my_books)
                                                                         
# Endpoint to get a specific book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in my_books if book['id'] == id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Endpoint to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.json
    my_books.append(new_book)
    return jsonify(new_book), 201

if __name__ == '__main__':
    app.run(debug=True)
