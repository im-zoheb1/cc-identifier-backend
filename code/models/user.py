from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(80))
    organization = db.Column(db.String(80))
    address = db.Column(db.String(180))
    password = db.Column(db.String(80))
    
    def __init__(self, username, email, organization, address, password):
        self.username = username
        self.email = email
        self.organization = organization
        self.address = address
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        #d
        return cls.query.filter_by(id=_id).first()