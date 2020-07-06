from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/drivers', methods=['GET', 'POST', 'DELETE'])
def login():
    if request.method == 'GET':
        return 'Sasai'
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


@app.route('/clients', methods=['GET', 'POST', 'DELETE'])
def login():
    if request.method == 'GET':
        return 'Sasai'
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


@app.route('/orders', methods=['GET', 'POST', 'DELETE'])
def login():
    if request.method == 'GET':
        return 'Sasai'
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


if __name__ == '__main__':
    app.run()
