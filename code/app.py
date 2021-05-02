from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = 'ccidentifier'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# JWT creates a new endpoint /auth
jwt = JWT(app, authenticate, identity)
 
# every resource have to be a class
class CCIdentifier(Resource):
    @jwt_required
    def get(self):
        return {'result': 'this is the result'}
    
api.add_resource(CCIdentifier, '/something')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)