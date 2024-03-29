from sqlalchemy.orm import backref, relationship
from db import db

class PatientModel(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    pre_existing_conditions = db.Column(db.String(80), default='NIL')
    age = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    result = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False, default='pending')
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    prescription = db.relationship("PrescriptionModel", backref=backref("prescriptions", uselist=False))

    def __init__(self, name, image, email, pre_existing_conditions, 
                 age, blood_group, result, status, user_id):
        self.name = name
        self.image = image
        self.email = email
        self.pre_existing_conditions = pre_existing_conditions
        self.age = age
        self.blood_group = blood_group 
        self.result = result 
        self.status = status
        self.user_id = user_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'email': self.email,
            'pre_existing_conditions': self.pre_existing_conditions,
            'age': self.age,
            'blood_group': self.blood_group,
            'result': self.result,
            'status': self.status,
        }

    # SAVES THE USER TO THE DATABASE
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    # GET PATIENT BY ID
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_status(cls, status):
        return cls.query.filter_by(status=status).all()
    
    @classmethod
    def find_pending_cases(cls, user_id):
        return cls.query.filter_by(user_id=user_id, status='pending')
    
    @classmethod
    def find_approved_cases(cls, user_id):
        return cls.query.filter_by(user_id=user_id, status='checked')