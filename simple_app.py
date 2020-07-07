from flask import Flask
from flask import request, Response
from flask import json
from database import Drivers

app = Flask(__name__)


@app.route('/drivers/<int:post_id>')
def shod_driver_profile(post_id):
    new_driver = Drivers()
    return str(new_driver.show_drivers(post_id))


@app.route('/drivers', methods=['POST', 'DELETE'])
def driver():
    try:
        new_driver = Drivers()
        json_from_request = json.loads(request.data.decode('utf-8'))
    except Exception:
        return Response('Произошла ошибка', status=400)
    if request.method == 'POST':
        try:
            new_driver.insert_drivers(json_from_request['name'], json_from_request['car'])
            return Response('Created', status=201)
        except Exception:
            return Response('Произошла ошибка', status=400)
    elif request.method == 'DELETE':
        print(json_from_request)
        print((json_from_request['id']))
        new_driver.delete_driver(json_from_request['id'])
        return Response('Deleted', status=201)


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
