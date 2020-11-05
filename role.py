from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.role import roleModel
from flask_jwt_extended import jwt_required



class roleData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    @jwt_required
    def post(self):
        data = roleData.parser.parse_args()


        role = roleModel(data['name'])

        try:
            role.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        # return Designation.json(), 201
