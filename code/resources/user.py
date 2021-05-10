from flask_restful import Resource, reqparse
from models.user import UserModel
from common.utils import validate_email, confirm_token, send_confirmation_mail

from passlib.hash import pbkdf2_sha256 # library for the password encryption

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required=True, 
        help='username cannot be blank'
    )
    parser.add_argument('email', 
        type=str,
        required=True, 
        help='email cannot be blank'
    )
    parser.add_argument('organization', 
        type=str,
        required=True, 
        help='organization cannot be blank'
    )
    parser.add_argument('address', 
        type=str,
        required=True, 
        help='address cannot be blank'
    )
    parser.add_argument('password', 
        type=str,
        required=True, 
        help='password cannot be blank'
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        
        if validate_email(data['email']):
            user = UserModel(
                data['username'], 
                data['email'], 
                data['organization'], 
                data['address'], 
                pbkdf2_sha256.hash(data['password']), # password encryption
                confirmed = False
            )

            send_confirmation_mail(data['email'], data['username'])

            user.save_to_db()
            
            return {'message': f'A confirmation email has been send to {data["email"]}. Please verify to continue.'}, 200
        else:
            return {"message": "Invalid Email"}, 422
        return
    
    
class UserVerification(Resource):
    def get(self, token):
        try:
            data = confirm_token(token)
        except:
            return {'message': 'Authentication token has expired'}, 401

        print('//////////////////////', data)

        user = UserModel.find_by_username(data['username'])

        if user.confirmed:
            return {'message': "Account is already verified"}, 400

        if user:
            user.confirmed=True
            user.save_to_db()
            return {'message': 'Your account has been verified'}, 200
        
        return {'message': 'FAILED: User not found'}, 404

# endpoint for testing purposes
class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200