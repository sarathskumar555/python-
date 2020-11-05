from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.department import departmentModel
from flask_jwt_extended import jwt_required


class department(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
# GETTING THE DETAILS BY ID
    @jwt_required
    def get(self, id):
        department = departmentModel.find_by_id(id)
        if department:
            if department.Status==True:
                    return department.json()
            else:
                return{"message":"no record found"},404
        else:
            return{"message":"no record found"},404




# DELETING THE DETAILS BY ID
    @jwt_required
    def delete(self, id):
        department = departmentModel.find_by_id(id)
        if department:
            if department.Status==True:
                user_data_del = departmentModel.update_by_status(id)
                data={
                "message":"record deleted",
                "id":department.id

                }
                return (data)
            else:
                return(' no record found'),404

        else:
            return("no record   found"),404


# UPADATING THE DETAILS BY ID
    @jwt_required
    def put(self,id):
        data = department.parser.parse_args()

        Department = departmentModel.find_by_id(id)

        if Department and Department.Status==True:

            Department.name = data['name']
            Department.save_to_db()

        else:
            return("no record found"),404

        return {"message": "department updated successfully ",'id':Department.id} , 201






# GETTING THE FULL DETAILS

class departmentList(Resource):
    @jwt_required
    def get(self):
        department=[]
        for x in departmentModel.query.filter_by(Status=True):
            department.append(x.json())

        return department











# POSTING THE DETAILS

class departmentData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required
    def post(self):
        data = department.parser.parse_args()
        if departmentModel.find_by_name(data['name']):
            return {'message': "A department with name '{}' already exists.".format(data['name'])}, 400



        Department = departmentModel(**data)


        try:
            Department.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {"message": "department created successfully ",'id':Department.id} , 201
