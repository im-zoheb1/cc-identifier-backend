from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.datastructures import FileStorage
from werkzeug.security import safe_str_cmp

import tensorflow as tf
from tensorflow import keras

from models.patients import PatientModel
from common.utils import validate_email, random_string

class Classifier(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
        type=str,
        required=True, 
        help='patient name cannot be blank'
    )
    parser.add_argument('image', 
        type=FileStorage,
        required=True, 
        help='image is required',
        location='files'
    )
    parser.add_argument('email', 
        type=str,
        required=True, 
        help='email cannot be blank'
    )
    parser.add_argument('pre_existing_conditions', 
        type=str,
        required=False,
        )
    parser.add_argument('age', 
        type=int,
        required=True, 
        help='age cannot be blank'
    )
    parser.add_argument('blood_group', 
        type=str,
        required=True, 
        help='blood group cannot be blank'
    )

    def cc_identifier(self, image, image_name):
        path_to_save = './assets/db_images'
        complete_path = f'{path_to_save}/{image_name}'
        image.save(complete_path)
        
        image_size = 32

        model = keras.models.load_model('./assets/trained_model')
        
        img = keras.preprocessing.image.load_img(complete_path, target_size=(image_size,image_size))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0)  # Create batch axis
        
        predictions = model.predict(img_array)
        score = predictions[0]
        result = '+ive' if (score[0] * 100) >= 50 else '-ive'

        return result

    @jwt_required(refresh=True)
    def post(self):
        data = Classifier.parser.parse_args()

        if validate_email(data['email']):
            image_name = f'{random_string()}.jpg'

            patient = PatientModel(
                data['name'],
                image_name,
                data['email'],
                data['pre_existing_conditions'], 
                data['age'], 
                data['blood_group'], 
                result = self.cc_identifier(data['image'], image_name), 
                status = 'pending',
                user_id = get_jwt_identity(),
            )
            patient.save_to_db()

            return {"message": "image has successfully been classified"}, 200
        return {"message": "Invalid email address"}, 422
    
class Patient(Resource):
    @jwt_required(refresh=True)
    def get(self, patient_id):
        patient = PatientModel.find_by_id(patient_id);
        
        # check if the patient does not exists
        if not(patient):
            return {"message": "Patient does not exist"}, 404
            
        user_id = get_jwt_identity()
        
        print(patient.user_id, user_id)
            
        if patient.user_id != user_id:
            return {"message": "You are not authorized to access this record"}, 403
            
        return patient.json(), 200 