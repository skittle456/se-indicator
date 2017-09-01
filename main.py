import configparser

from flask import (
    Flask,
)

from apis import api
from line.in_event import CryptoBot
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
api.init_app(app)

currencies = ["BTC", "ETH", "DAS", "OMG", "XRP"]
cryptoBot = CryptoBot(currencies)
print('cryptoBot created ja')
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response


if __name__ == "__main__":
    #app.run(host="0.0.0.0")
    #app.run(host="127.0.0.1")
    app.run()
