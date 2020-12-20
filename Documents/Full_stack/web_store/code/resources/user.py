import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help='This field can not be empty')
    parser.add_argument('password', type=str, required=True,
                        help='This field can not be empty')

    def post(self):
        data = UserRegister.parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        if user is None:
            user = UserModel(**data)
        else:
            return {'message': 'User with name {} already exist'.format(data['username'])}, 400
        user.save_to_db()

        return {'message': 'User has been created'}, 201
