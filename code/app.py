from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager


from config import BaseConfig
from blacklist import BLACKLIST


from resources.patients import (
    Classifier,
    Patient,
    PatientPending,
    PatientChecked,
    PatientPublic
)

from resources.user import (
    User, 
    UserRegister, 
    UserVerification,
    UserLogin,
    UserLogout, 
    TokenRefresh,
    ResendConfirmation,
    ChangePassword
)

from resources.prescriptions import Prescription

app = Flask(__name__)

app.config['SECRET_KEY'] = BaseConfig.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = BaseConfig.DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = BaseConfig.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['PROPAGATE_EXCEPTIONS'] = BaseConfig.PROPAGATE_EXCEPTIONS
app.config['JWT_BLACKLIST_ENABLED'] = BaseConfig.JWT_BLACKLIST_ENABLED
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = BaseConfig.JWT_BLACKLIST_TOKEN_CHECKS

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# won't create /auth endpoint
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(self, decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_loader():
    return jsonify({
        'description': 'The token has expired',
        'error': 'token_expired'
    }), 401
    
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401 

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain any access token',
        'error': 'authorization_required'
    }), 401 

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'Token is not fresh',
        'error': 'fresh_token_required'
    }), 401 
 
api.add_resource(UserRegister, '/register')
api.add_resource(UserVerification, '/confirm/<string:token>')
api.add_resource(User, '/user')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ResendConfirmation, '/resend_confirmation/<string:username>')
api.add_resource(ChangePassword, '/change_password')

api.add_resource(Prescription, '/prescription/<int:patient_id>')

api.add_resource(Classifier, '/classifier')
api.add_resource(Patient, '/patient/<string:patient_id>')
api.add_resource(PatientPublic, '/patient_public/<string:patient_id>')
api.add_resource(PatientPending, '/patient/pending')
api.add_resource(PatientChecked, '/patient/checked')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)