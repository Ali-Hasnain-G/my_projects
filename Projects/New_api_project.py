from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def name():
    return jsonify('your name is this')





if __name__ == '__main__':
    app.run(debug=True)
