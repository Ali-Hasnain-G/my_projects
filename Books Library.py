from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Read the CSV file into a pandas DataFrame
my_books_df = pd.read_csv(r"F:\Full Stack Development\datasets\Bookss.csv")

# Convert the DataFrame to a list of dictionaries
books_dict = my_books_df.to_dict(orient='records')

# Display the first few rows of the DataFrame
print(books_dict[:5])

# Error handler for invalid routes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not Found"}), 404


# Endpoint to get all books
@app.route('/my_books', methods=['GET'])
def get_books():
    return jsonify(books_dict)

# Endpoint to get a specific book by ID
@app.route('/my_books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in books_dict if book['id'] == id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"No": "Book not found"}), 404

# Endpoint to add a new book
@app.route('/my_books', methods=['POST'])
def add_book():
    new_book = request.json
    books_dict.append(new_book)
    # Optionally, update the DataFrame if you need to save it back to CSV
    # my_books_df = pd.DataFrame(books_dict)
    return jsonify(new_book), 201

# Endpoint to update a book by ID
@app.route('/my_books/<int:id>', methods=['PUT'])
def update_book(id):
    updated_book = request.json
    for i, book in enumerate(books_dict):
        if book['id'] == id:
            books_dict[i] = updated_book
            return jsonify(updated_book)
    return jsonify({"error": "Book not found"}), 404

# Endpoint to delete a book by ID
@app.route('/my_books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books_dict
    books_dict = [book for book in books_dict if book['id'] != id]
    return jsonify({"Ok": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
