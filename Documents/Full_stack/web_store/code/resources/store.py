from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask_restful import reqparse, Resource
from models.store import StoreModel


class Store (Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=float, required=True,
                        help='This field cannot be blank')
    # parser.add_argument('store_id', type=int, required=True,
    #                     help='Every item need a store id')

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 201
        return {'message': 'Item not found'}, 400

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'item': 'An item with name {} was found'.format(name)}, 400
        data = Store.parser.parse_args()
        store = StoreModel(name, **data)

        try:
            store.save_to_db()
        except:
            return{'message': 'An error occured while inserting item'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_to_db()
        return {'message': 'item has been deleted'}

    @jwt_required()
    def put(self, name):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(name)

        if store is None:
            store = StoreModel(name, **data)
        else:
            store.price = data['price']
        store.save_to_db()
        return store.json(), 200


class StoreList (Resource):
    @jwt_required()
    def get(self):
        # return {'items': list(map(lambda item: item.json(), ItemModel.query.all()))}
        return {'items': [store.json() for store in StoreModel.query.all()]}
