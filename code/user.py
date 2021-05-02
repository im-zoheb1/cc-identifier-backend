import sqlite3
from flask_restful import Resource, reqparse

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
    @classmethod # means that now we are using the current class
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username, ))
        
        # taking out the first row out of the result
        row = result.fetchone() 
        if row: 
            user = cls(*row) # cls here will be the class 'User'
            # '*row' passing as set of arguments
        else: 
            user = None
            
        connection.close()
        return user
    
    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id, ))

        row = result.fetchone() 
        if row: 
            user = cls(*row)
        else: 
            user = None
            
        connection.close()
        return user
        
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username', 
        type=str,
        required=True, 
        help='username cannot be blank'
    )
    parser.add_argument(
        'email', 
        type=str,
        required=True, 
        help='email cannot be blank'
    )
    parser.add_argument(
        'organization', 
        type=str,
        required=True, 
        help='organization cannot be blank'
    )
    parser.add_argument(
        'address', 
        type=str,
        required=True, 
        help='address cannot be blank'
    )
    parser.add_argument(
        'password', 
        type=str,
        required=True, 
        help='password cannot be blank'
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_username(data['username']):
            return {'message': "A user with this name already exists"}
        
        data = UserRegister.parser.parse_args()
        
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)"
        cursor.execute(query, (data['username'], data['email'], data['organization'], data['address'], data['password']))

        connection.commit()
        connection.close()
        
        return {"message": "user was created successfully"}, 201