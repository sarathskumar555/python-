from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# from models.role import roleModel
from flask_jwt_extended import jwt_required
from flask import request
from verify_email import verify_email
from emailverifier import Client
from emailverifier import exceptions



class email(Resource):

    # @jwt_required
    def post(self):
        data = request.get_json()
        verify=verify_email(data['email'])
        if verify==True:
            return('verified')
        else:
            return("not verified")
