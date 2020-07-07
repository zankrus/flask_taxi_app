from flask import Flask
from flask import request, Response
from flask import json
from database import Drivers, Clients, Orders

app = Flask(__name__)


@app.route('/drivers/<int:post_id>')
def show_driver_profile(post_id):
    try:
        new_driver = Drivers()
        resp = str(new_driver.show_drivers(post_id))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return str(resp)
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
    try:
        new_client = Clients()
        resp = str(new_client.show_clients(client_id))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return resp
    except Exception:
        return Response('Неправильный запрос', status=400)


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
            return Response('Неправильный запрос', status=400)
    elif request.method == 'DELETE':
        try:
            print(json_from_request)
            print((json_from_request['id']))
            if str(new_client.show_clients(json_from_request['id'])) == '[]':
                return Response('Объект не найден в базе', status=404)
            new_client.delete_clients(json_from_request['id'])
            return Response('Deleted', status=201)
        except Exception:
            return Response('Неправильный запрос', status=400)


@app.route('/orders/<int:order_id>')
def show_order(order_id):
    try:
        new_order = Orders()
        resp = str(new_order.show_order(order_id))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return str(resp)
    except Exception:
        return Response('Неправильный запрос', status=400)


@app.route('/orders', methods=['POST', 'PUT'])
def order():
    try:
        new_order = Orders()
        json_from_request = json.loads(request.data.decode('utf-8'))
    except Exception:
        return Response('Произошла ошибка', status=400)
    if request.method == 'POST':
        try:
            new_order.insert_order(json_from_request['address_from'], json_from_request['address_to'],
                                   json_from_request['client_id'],
                                   json_from_request['driver_id'],
                                   json_from_request['date_created'], json_from_request['status']
                                   )
            return Response('Created', status=201)
        except ValueError:
            return Response('Неправильный запрос', status=400)
    elif request.method == 'PUT':
        pass


if __name__ == '__main__':
    app.run()
