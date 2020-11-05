from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import datetime

# from security import authenticate, identity
from resources.department import department,departmentList,departmentData
from resources.designation import designation,designationList,designationData
from resources.user import user,userList,userData,login,change_Password,forgetPassword,resetPassword,TokenRefresh
from resources.survey import survey,surveyList,surveyData
from resources.question import question,questionList,questionData,Options,OptionsRemove
from resources.surveyquestion import surveyquestion,surveyquestionList,surveyquestionData
from resources.surveyresponse import surveyresponseData,surveyresponse,surveyresponseList,surveyresponseFilter
from resources.auditlog import auditlogData,auditlog
from resources.role import roleData
from resources.login import email
from flask_jwt_extended import jwt_required,get_raw_jwt,jwt_refresh_token_required



app = Flask(__name__)
app.config.from_object("config.Config")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///surveysystem.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'thomas'
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# app.secret_key = 'jose'
Port=app.config["PORT"]
Host=app.config["HOST"]
api = Api(app)



@app.before_first_request
def create_tables():
    db.create_all()

# app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWTManager(app)  # /auth
blacklist = set()
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist








api.add_resource(department, '/api/v1/department/<int:id>')
api.add_resource(departmentList, '/api/v1/department')
api.add_resource(departmentData, '/api/v1/department')
api.add_resource(designation, '/api/v1/designation/<int:id>')
api.add_resource(designationList, '/api/v1/designation')
api.add_resource(designationData, '/api/v1/designation')
api.add_resource(user, '/api/v1/user/<int:id>')
api.add_resource(userList, '/api/v1/user')
api.add_resource(userData, '/api/v1/user')
api.add_resource(login, '/api/v1/login')
api.add_resource(change_Password, '/api/v1/changePassword/<int:id>')
api.add_resource(survey, '/api/v1/survey/<int:id>')
api.add_resource(surveyList, '/api/v1/survey')
api.add_resource(surveyData, '/api/v1/survey')
api.add_resource(question, '/api/v1/question/<int:id>')
api.add_resource(questionList, '/api/v1/question')
api.add_resource(questionData, '/api/v1/question')
api.add_resource(OptionsRemove, '/api/v1/question/<int:id>/<int:question_id>')
api.add_resource(Options, '/api/v1/optionadd/<int:id>')
api.add_resource(surveyquestion, '/api/v1/surveyquestion/<int:id>')
api.add_resource(surveyquestionList, '/api/v1/surveyquestion/<int:survey_id>/<int:question_id>')
# api.add_resource(surveyquestionList, '/api/v1/surveyquestion')
api.add_resource(surveyquestionData, '/api/v1/surveyquestion')
api.add_resource(surveyresponse, '/api/v1/surveyresponse/<int:survey_id>')
api.add_resource(surveyresponseFilter, '/api/v1/surveylist/<int:user_id>')
api.add_resource(surveyresponseList, '/api/v1/surveyresponse/<int:survey_id>/<int:user_id>')
api.add_resource(surveyresponseData, '/api/v1/surveyresponse')
api.add_resource(auditlogData, '/api/v1/auditlog')
api.add_resource(auditlog, '/api/v1/auditlog/<string:name>')
api.add_resource(roleData, '/api/v1/role')
api.add_resource(TokenRefresh, '/api/v1/refresh')
api.add_resource(forgetPassword, '/api/v1/forgetPassword')
api.add_resource(resetPassword, '/api/v1/resetPassword/<int:user_id>/<string:accesstoken>')
# api.add_resource(auditlogData, '/api/v1/auditlog/<string:name>/<string:page>/<string:fromDate>/<string:toDate>')


@app.route('/api/v1/logout', methods=['DELETE'])
@jwt_refresh_token_required
# @jwt_required

def logout():
    jti = get_raw_jwt()['jti']
    print("sarathsssss",jti)
    blacklist.add(jti)
# @jwt_required
# def logout2():
#     jti = get_raw_jwt()['jti']
#     blacklist.add(jti)


    return{"msg": "Successfully logged out"}, 200

# @app.route('/api/v1/refreshlogout', methods=['DELETE'])
# @jwt_refresh_token_required
# def logout2():
#     jti = get_raw_jwt()['jti']
#     blacklist.add(jti)
#     return {"msg": "Successfully logged out"}, 200







if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=Port,host=Host, debug=True)
