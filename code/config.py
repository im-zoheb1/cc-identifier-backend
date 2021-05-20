class BaseConfig():
    # BASE CONFIGURATION
    SECRET_KEY = 'ccidentifier'
    SECURITY_PASSWORD_SALT = 'my_passw0ord_salt'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    DB_PATH = 'sqlite:///data.db'
    MAIL_SERVER = 'smtp.gmail.com:587'
    
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
