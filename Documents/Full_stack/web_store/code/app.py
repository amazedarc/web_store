from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask('__name__')
app.secret_key = 'mazina'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []


class Item (Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field cannot be blank')

    @jwt_required()
    def get(self, name):

        item = next(filter(lambda item: item['name'] == name, items), None)
        return {"item": item}, 202 if item else 404

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': 'An item with name {} was found'.format(name)}, 400

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return items, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        data = Item.parser.parse_args()
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList (Resource):
    @jwt_required()
    def get(self):
        return {"items": items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=4400, debug=True)
