from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserVerification, User, UserLogin

from config import BaseConfig

app = Flask(__name__)

app.config['SECRET_KEY'] = BaseConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = BaseConfig.DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = BaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['PROPAGATE_EXCEPTIONS'] = BaseConfig.PROPAGATE_EXCEPTIONS

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# won't create /auth endpoint
jwt = JWTManager(app)
 
api.add_resource(UserRegister, '/register')
api.add_resource(UserVerification, '/confirm/<string:token>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)