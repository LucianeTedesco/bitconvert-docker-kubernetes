import os
import requests
from bs4 import BeautifulSoup
from flask import Flask,jsonify

app = Flask(__name__)

BITCOIN_ENDPOINT = os.getenv('BITCOIN_ENDPOINT', 'http://localhost:5001')

@app.route("/dolar")
def buscarPrecoDolar():

    req = requests.get('https://www.dolarhoje.com/')

    if (req.status_code == 200):
        content = req.content

        soup = BeautifulSoup(content, 'html.parser')
        valorDolarReal = soup.find(name='input', attrs={'id': 'nacional'})

        return jsonify(valor=valorDolarReal.attrs.get('value'))
    return jsonify(erro='falha na requisicao')


@app.route("/dolarbitcoin")
def getBitCoinValue():
    responseReal = requests.get('http://localhost:5000/dolar')
    responseDolar = requests.get(f'{BITCOIN_ENDPOINT}/bitcoin')
    return float(responseDolar.json()[0].get('valor')) * float(responseReal.json()[0].get('valor'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
