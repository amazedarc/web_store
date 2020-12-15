from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask('__name__')
app.secret_key = 'mazina'
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []


class Item (Resource):
    @jwt_required()
    def get(self, name):

        item = next(filter(lambda item: item['name'] == name, items), None)
        return {"item": item}, 202 if item else 404

    def post(self, name):
        if next(filter(lambda item: item['name'] == name, items), None):
            return {'message': 'An item with name {} was found'.format(name)}, 400

        request_data = request.get_json()
        item = {'name': name, 'price': request_data['price']}
        items.append(item)
        return items, 201


class ItemList (Resource):
    def get(self):
        return {"items": items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=4400, debug=True)
