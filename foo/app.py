import os
import requests

from flask import Flask

app = Flask(__name__)

BAR_ENDPOINT = os.getenv('BAR_ENDPOINT', 'http://localhost:5001')

@app.route("/foo")
def foo():
    return "foo"


@app.route("/foobar")
def bar():
    response = requests.get(f'{BAR_ENDPOINT}/bar')
    return "foo" + response.text


if __name__ == '__main__':
    app.run(host='0.0.0.0')
