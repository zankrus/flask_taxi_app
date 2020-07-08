"""Flask app."""
from flask import Flask
from flask import request, Response
from flask import json
from database import Drivers, Clients, Orders, striper
from typing import Any

app = Flask(__name__)


@app.route('/drivers/<int:post_id>')
def show_driver_profile(post_id: int) -> Any:
    """Funct for show drivers by id."""
    try:
        new_driver = Drivers()
        resp = str(new_driver.show_drivers(post_id))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return str(resp)
    except Exception:
        return Response('Неправильный запрос', status=400)


@app.route('/drivers', methods=['POST', 'DELETE'])
def driver() -> Response:
    """Func for delete and add to drivers."""
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
    else:
        return Response('Неправильный запрос', status=400)


@app.route('/clients/<int:client_id>')
def show_client_profile(client_id: int) -> Any:
    """Func for show clients."""
    try:
        new_client = Clients()
        resp = str(new_client.show_clients(client_id))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return resp
    except Exception:
        return Response('Неправильный запрос', status=400)


@app.route('/clients', methods=['POST', 'DELETE'])
def client() -> Response:
    """Func for add and delete clients."""
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
    else:
        return Response('Неправильный запрос', status=400)


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT'])
def show_order(order_id: int) -> Any:
    """Func for show orders."""
    try:
        new_order = Orders()
        resp = str(new_order.show_order(order_id))
    except Exception:
        return Response('Неправильный запрос', status=400)
    if request.method == 'GET':
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        return str(resp)
    if request.method == 'PUT':
        json_from_request = json.loads(request.data.decode('utf-8'))
        if resp == '[]':
            return Response('Объект не найден в базе', status=404)
        print(striper(resp)['status'])
        print(json_from_request['status'])
        if striper(resp)['status'] == 'not_accepted' and json_from_request['status'] in ['in progress', 'cancelled']:
            new_order.update_orders_not_accepted(order_id,
                                                 json_from_request['status'],
                                                 json_from_request['date_created'],
                                                 json_from_request['driver_id'],
                                                 json_from_request['client_id'])
            return Response('Изменено', status=200)
        elif striper(resp)['status'] == 'in progress' and json_from_request['status'] in ['done', 'cancelled']:
            new_order.update_orders(order_id,
                                    json_from_request['status'])
            return Response('Изменено', status=200)
        return Response('Неверная последовательность статусов', status=400)


@app.route('/orders', methods=['POST'])
def order() -> Response:
    """Func for add  orders."""
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
    else:
        return Response('Неправильный запрос', status=400)


if __name__ == '__main__':
    app.run()
