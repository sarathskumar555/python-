from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.designation import designationModel
from flask_jwt_extended import jwt_required
from models.user import userModel
from flask import request


class designation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

# GETTING THE DETAILS BY ID
    def get(self, id):
        # token = request.headers.get('Authorization')
        # split_token = token.split("Bearer ")[1]
        # data = userModel.find_by_token(split_token)
        # if data and data.accesstoken == split_token:
            designation = designationModel.find_by_id(id)
            if designation:
                if designation.Status==True:
                        return designation.json()
                else:
                    return {'message': 'designation not found'}, 404
            else:
                return("designation not found"),404




# DELETING THE DETAILS BY ID

    @jwt_required
    def delete(self,id):
        designation =designationModel.find_by_id(id)
        if designation:
            if designation.Status==True:
                designation.update_by_status(id)
                data={
                "message":"record deleted",
                "id":designation.id

                }
                return (data)
            else:
                return {'message': 'designation not found.'}, 404
        else:
                return{"message":"no record found"},404

# UPDATING THE DETAILS BY ID

    @jwt_required
    def put(self,id):
        data = designation.parser.parse_args()

        Designation = designationModel.find_by_id(id)

        if Designation and Designation.Status==True:

            Designation.name = data['name']
            Designation.save_to_db()
        else:
            return{"message":"no record found"},404


        return {"message": "designation updated successfully ",'id':Designation.id} , 201

# GETTING THE FULL DETAILS
class designationList(Resource):
    @jwt_required
    def get(self):
        Designation=[]
        for x in designationModel.query.filter_by(Status=True):
            Designation.append(x.json())

        return Designation


# POSTING THE DETAILS
class designationData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @jwt_required
    def post(self):
        data = designationData.parser.parse_args()
        if designationModel.find_by_name(data['name']):
            return {'message': "A designation with name '{}' already exists.".format(data['name'])}, 400

        Designation = designationModel(data['name'])

        try:
            Designation.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {"message": "designation created successfully ",'id':Designation.id} , 201
