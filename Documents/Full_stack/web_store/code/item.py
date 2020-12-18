from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required
from flask_restful import reqparse, Resource


class Item (Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help='This field cannot be blank')
    # parser.add_argument('name', type=str, required=True,
    #                     help='This field cannot be blank')

    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT *  FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            return{'item': {'id': row[0], 'name': row[1], 'price': row[2]}}, 201
        connection.close()
        return {'message': 'Item not found'}, 400

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'id': row[0], 'name': row[1], 'price': row[2]}}

    @classmethod
    def insert(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (NULL,?,?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        data = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    @jwt_required()
    def post(self, name):
        if self.find_by_name(name):
            return {'item': 'An item with name {} was found'.format(name)}, 400
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return{'message': 'An error occured while inserting item'}, 500
        return {'message': 'the Item has been created'}, 201

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'item has been deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)

        updated_item = {'name': name, 'price': data['price']}
        if item:
            self.update(updated_item)
        else:
            self.insert(updated_item)
        return {'message': 'item has been updated'}, 200


class ItemList (Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT *  FROM items'
        result = cursor.execute(query)
        items = []
        for item in result:
            items.append({'id': item[0], 'name': item[1], 'price': item[2], })
        return {'items': items}, 201
        connection.close()
