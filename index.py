from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "<?xml version='1.0' encoding='UTF-8'?><Response><Message>Hello from GoGo Home!</Message></Response>"


if __name__ == '__main__':
    app.run(debug=True, port=5656)