from db import db

class PrescriptionModel(db.Model):
    __tablename__ = 'prescriptions'

    id = db.Column(db.Integer, primary_key=True)
    clinic = db.Column(db.String(80), nullable=False)
    prescription = db.Column(db.String, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))

    

    def __init__(self, clinic, prescription, patient_id):
        self.clinic = clinic    
        self.prescription = prescription
        self.patient_id = patient_id

    def json(self):
        return {
            'clinic': self.clinic,
            'prescription': self.prescription,
        }

    # SAVES THE SUGGESTED TREATMENT TO DATABASE
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    # GET PATIENT BY ID
    @classmethod
    def find_by_patient_id(cls, _id):
        return cls.query.filter_by(patient_id=_id).first()