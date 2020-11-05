from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.surveyresponse import surveyresponseModel
from models.user import userModel
from datetime import datetime
from flask import request,jsonify
from models.question import questionModel
from models.survey import surveyModel
from models.options import optionsModel
from models.auditlog import auditlogModel
from flask_jwt_extended import jwt_required


# GETTING THE DETAILS USING SURVEYID
class surveyresponse(Resource):

    @jwt_required
    def get(self,survey_id):
        survey=surveyresponseModel.find2_by_id(survey_id)

        # print(survey)
        user=userModel.find2_by_id()
        print("ss")
        # flag=s.name
        arr1=[]
        if survey:
            for x in user:
                 data={
                      "user_id":x.id,
                     "name":x.name,
                    "status":"non attended"
                    }

                 for y in survey:

                    if x.id==y.user_id:
                        data={
                        "user_id":x.id,
                        "name":x.name,
                        "status":"attended"
                        }
                    #
                    # else:
                    #
                 arr1.append(data)

            return(arr1)
        else:
            return{"message":"No option for the respective survey "}







# GETTING THE DETAILS BY SURVEYID ,USERID

class surveyresponseList(Resource):
    @jwt_required
    def get(self,survey_id,user_id):
        survey =surveyresponseModel.find3_by_id(survey_id,user_id)
        # print(survey.id)
        # question=questionModel.find3_by_id()
        data1=[]
        if survey:
            for x in survey:
                question=questionModel.find_by_id(x.question_id)
                user=userModel.find_by_id(x.user_id)
                survey1=surveyModel.find_by_id(x.survey_id)
                option1=optionsModel.find_by_id(x.option)
                print("sarathsssss",option1.options)
                # print(question.description)
                que_des=question.description
                user_name=user.name
                survey1=survey1.name
                option=option1.options
                data5={
                "questionID":x.question_id,
                "question":question.description
                }
                data6={
                "optionID":x.option,
                "option":option1.options
                }

                # print(survey.user_id)
                data ={
                "id":x.id,
                "question":data5,
                "option":data6
                }
                data1.append(data)
            data2={
            "employee name":user_name,
            "survey name":survey1,
            "results":data1
            }
            return(data2)
        else:
            return{"message":'user have no option on respective survey'}







# POSTING THE DETAILS
class surveyresponseData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('survey_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('question_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('start_date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('end_date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('option',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )



    @jwt_required
    def post(self):
        data = surveyresponseData.parser.parse_args()
        if surveyresponseModel.find4_by_id(data['survey_id'],data['question_id'],data['user_id']):
            return {"message": "Already exists"}, 400


        start = datetime.strptime(data['start_date'], '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.strptime(data['end_date'], '%Y-%m-%d %H:%M:%S.%f')
        # print(type(data['user_id']))
        Survey = surveyresponseModel(data['survey_id'],data['user_id'],data['question_id'],start,end,data['option'])

        print(type(start))

        try:
            # print("SARATH")
            Survey.save_to_db()

        except:

            return {"message": "An error occurred inserting the item."}, 500

        action="survey attended"
        page="survey"
        id=data['user_id']
        audit=auditlogModel(id,action,page)
        try:
            audit.save_to_db()
        except:
                return {"message": "An error occurred inserting the item."}, 500


        str1=str(start)
        str2=str(end)
        data ={
        "message":"option recorded",
        "id":Survey.id
        }

        return(data)



class surveyresponseFilter(Resource):

    @jwt_required
    def get(self,user_id):
        survey=surveyresponseModel.find5_by_id(user_id)
        date=datetime.now()

        # print(survey)
        # survey2=surveyModel.find5_by_id()
        survey3=surveyModel.query.filter(surveyModel.Status==True, surveyModel.end_Date >= date)
        # print(user)
        arr1=[]
        if survey:
            if survey3:
                for x in survey3:
                     data={
                          "id":x.id,
                         "name":x.name,
                        "status":"non attended"
                        }

                     for y in survey:

                        if x.id==y.survey_id:
                            data={
                            "id":x.id,
                            "name":x.name,
                            "status":"attended"
                            }
                        #
                        # else:
                        #
                     arr1.append(data)

                return{"Active survey":arr1}
            else:
                return{"message":"No active survey"}

        else:
            return{"message":"No such user found"}










# date=datetime.now()
#         survey=SurveyResponseModel.find5_by_id(userId)
#         #.find5_by_id()   query.filter(SurveyQuestionModel.surveyId==id,SurveyQuestionModel.Status==True)))
#         survey2=SurveyModel.query.filter(SurveyModel.Status==True, SurveyModel.enddate >= date)
