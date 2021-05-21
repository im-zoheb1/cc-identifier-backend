from passlib.hash import pbkdf2_sha256 # library for the password encryption
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    get_jwt_identity,
    jwt_required,
    get_jwt
)

from models.user import UserModel
from common.utils import validate_email, confirm_token, send_confirmation_mail
from blacklist import BLACKLIST

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

        if UserModel.find_by_email(data['email']):
            return {"message": "This email address is already occupied. Please use a different email_address"}, 400
        
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

class ResendConfirmation(Resource):
    def post(self, username):
        user = UserModel.find_by_username(username)
        if user.confirmed:
            return {"message": "Account is already verified. Please login to continue."}
        send_confirmation_mail(user.email, user.username)
        return {"message": f"Confirmation has been been to {user.email}."}, 200


class UserVerification(Resource):
    def get(self, token):
        data = confirm_token(token)
        if not(data):
            return {'message': 'Authentication token has expired'}, 401

        # try:
        #     data = confirm_token(token)
        # except:
        #     return {'message': 'Authentication token has expired'}, 401

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


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', 
        type=str,
        required=True, 
        help='username cannot be blank'
    )
    parser.add_argument('password', 
        type=str,
        required=True, 
        help='password cannot be blank'
    )
    @classmethod
    def post(cls):
        # get data from parser
        data = cls.parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        # this is what the authenticate() function used to do 
        if not(user.confirmed):
            return {'message': 'Please verify your account to sign in.', 'error':'unverified-account'}, 403
        
        if user and pbkdf2_sha256.verify(data['password'], user.password):
            # identity= is what the 'identity()' function used to do 
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token # refresh token is never going to change
            }, 200
        
        return {'message': 'Invalid credentials'}, 401
    
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token', new_token}, 200

class UserLogout(Resource):
    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti'] # jti is "JWT ID", a unique identifier for JWT
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200
    