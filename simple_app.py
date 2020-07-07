from flask import Flask
from flask import request, Response
from flask import json
from database import Drivers, Clients

app = Flask(__name__)


@app.route('/drivers/<int:post_id>')
def show_driver_profile(post_id):
    try:
        new_driver = Drivers()
        resp = str(new_driver.show_drivers(post_id))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return resp
    except Exception:
        return Response('Неправильный запрос', status=400)


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
            print('Post' + str(json_from_request))
            return Response('Created', status=201)
        except Exception:
            return Response('Неправильный запрос', status=400)
    elif request.method == 'DELETE':
        try:
            print('Delete')
            print(json_from_request)
            if str(new_driver.show_drivers(json_from_request['id'])) == '[]':
                return Response('Объект не найден в базе', status=404)
            new_driver.delete_driver(json_from_request['id'])
            return Response('Удалено', status=204)
        except Exception:
            return Response('Неправильный запрос', status=400)


@app.route('/clients/<int:client_id>')
def show_client_profile(client_id):
    new_client = Clients()
    return str(new_client.show_clients(client_id))


@app.route('/clients', methods=['POST', 'DELETE'])
def client():
    try:
        new_client = Clients()
        json_from_request = json.loads(request.data.decode('utf-8'))
    except Exception:
        return Response('Произошла ошибка', status=400)

    if request.method == 'POST':
        try:
            new_client.insert_clients(json_from_request['name'], json_from_request['is_vip'])
            return Response('Created', status=201)
        except Exception:
            return Response('Произошла ошибка', status=400)
    elif request.method == 'DELETE':
        print(json_from_request)
        print((json_from_request['id']))
        new_client.delete_clients(json_from_request['id'])
        return Response('Deleted', status=201)


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
