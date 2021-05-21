from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.prescriptions import PrescriptionModel
from models.patients import PatientModel

class Prescription(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('clinic', 
        type=str,
        required=True, 
        help='clinic suggesstion is required'
    )
    parser.add_argument('prescription', 
        type=str,
        required=True, 
        help='prescription is required',
    )
    
    @jwt_required(refresh=True)
    def post(self, patient_id):
        
        if PrescriptionModel.find_by_patient_id(patient_id):
            return {"message": "Treatment has already been suggested"}, 400
        
        # WRITE PRESCRIPTIONS TO THE PATIENT
        data = Prescription.parser.parse_args()
        prescription = PrescriptionModel(**data, patient_id=patient_id)

        # UPDATE THE PATIENT REPORT STATUS
        try:
            patient = PatientModel.find_by_id(patient_id)
            patient.status = 'checked'
        except:
            return {'message': 'The patient you are writing prescription for does not exist'}, 400
        
        prescription.save_to_db()
        patient.save_to_db()
        
        return {'message': 'successful'}, 200