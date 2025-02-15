from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

if __name__ == '__main__':
    # debug=True enables auto-reloading of the server when you make code changes
    app.run(debug=True)

