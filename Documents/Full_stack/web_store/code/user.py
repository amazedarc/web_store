class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    def json(self):

        return {
            'id': self.id,
            'username': self.username,
            'password': self.passowrd
        }
