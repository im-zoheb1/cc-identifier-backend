from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister

app = Flask(__name__)
app.secret_key = 'ccidentifier'
api = Api(app)

# JWT creates a new endpoint /auth
jwt = JWT(app, authenticate, identity)
 
# every resource have to be a class
class CCIdentifier(Resource):
    @jwt_required
    def get(self):
        return {'result': 'this is the result'}
    
api.add_resource(CCIdentifier, '/something')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)