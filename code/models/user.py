from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    organization = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(180), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False) # confirming if signup is verified
 
    patient = db.relationship('PatientModel', backref='user', lazy='dynamic')

    def __init__(self, username, email, organization, address, password, confirmed):
        self.username = username
        self.email = email
        self.organization = organization
        self.address = address
        self.password = password
        self.confirmed = confirmed # confirming if signup is verified
    
    def json(self):
        return {
            'username': self.username,
            'email': self.email,
            'organization': self.organization,
            'address': self.address,
        }
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    # saves the user to the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()