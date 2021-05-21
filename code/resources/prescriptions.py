from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.prescriptions import PrescriptionModel

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
        data = Prescription.parser.parse_args()
        prescription = PrescriptionModel(**data, patient_id=patient_id)
        prescription.save_to_db()
        return {'message': 'successful'}, 200