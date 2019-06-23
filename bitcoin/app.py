import os
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify

app = Flask(__name__)


@app.route("/bitcoin")
def buscarPrecoBitcoin():
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')

    if (response.status_code == 200):
        valorBitcoin = response.json()[0].get('price_usd')
        return jsonify(valor=valorBitcoin)
    return jsonify(erro='Bad request')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
