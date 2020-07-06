from flask import Flask
from flask import request, Response
from flask import json
from database import Drivers

app = Flask(__name__)


@app.route('/drivers', methods=['GET', 'POST', 'DELETE'])
def driver():
    try:
        new_driver = Drivers()
        json_from_request = json.loads(request.data.decode('utf-8'))
    except Exception:
        return Response('Произошла ошибка', status=400)
    if request.method == 'GET':
        new_driver.show_drivers('name')
        return 'Sasai'
    elif request.method == 'POST':
        try:
            new_driver.insert_drivers(json_from_request['name'], json_from_request['car'])
            return Response('Created', status=201)
        except Exception:
            return Response('Произошла ошибка', status=400)
    elif request.method == 'DELETE':
        pass


@app.route('/clients', methods=['GET', 'POST', 'DELETE'])
def client():
    if request.method == 'GET':
        return 'Sasai'
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


@app.route('/orders', methods=['GET', 'POST', 'DELETE'])
def order():
    if request.method == 'GET':
        return 'Sasai'
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


if __name__ == '__main__':
    app.run()
