import os
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify

app = Flask(__name__)


@app.route("/bitcoin")
def buscarPrecoBitcoin():
    req = requests.get('https://www.coindesk.com/price/bitcoin')

    if (req.status_code == 200):
        content = req.content

        soup = BeautifulSoup(content, 'html.parser')
        valorBitcoinDolar = soup.find(name='span', attrs={'class': 'push-data'})

        return jsonify(valor=valorBitcoinDolar.attrs.get('value'))
    return jsonify(erro='falha na requisicao')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
