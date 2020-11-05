from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.survey import surveyModel
from datetime import datetime
from flask import request,jsonify
from flask_jwt_extended import jwt_required
from models.surveyquestion import surveyquestionModel


class survey(Resource):

# GETTING THE DETAILS BY ID
    @jwt_required
    def get(self, id):
        survey = surveyModel.find_by_id(id)

        if survey and survey.Status==True:
            str1 =str(survey.start_Date)
            str2 =str(survey.end_Date)
            data ={
            "id":survey.id,
            "name":survey.name,
            "description":survey.description,
            "thank_you_message":survey.thank_you_message,
            "end_Date":str2,
            "start_Date":str1}
            return (data)


        else:
             return {'message': 'survey not found'}, 404






# DELETING THE DETAILS BY ID

    @jwt_required
    def delete(self, id):
        survey = surveyModel.find_by_id(id)
        if survey and survey.Status==True:
            sur_que=surveyquestionModel.query.all()
            # print(sur_que)
            for x in sur_que:
                if x.survey_id==id:
                    x.Status=False



            deleted = surveyModel.update_by_status(id)

            str1 =str(survey.start_Date)
            str2 =str(survey.end_Date)
            data ={
            "message":"record deleted",
            "id":survey.id
            }

            return(data)
        else:
            return {'message': 'survey not found.'}, 404








# UPDATING THE DETAILS BY ID
    @jwt_required
    def put(self,id):
        data =request.get_json()

        Survey = surveyModel.find_by_id(id)
        # print('ssssssssss',type(data['end_Date']))

 # datetime.strptime(ss, '%Y-%m-%d %H:%M:%S.%f')
        if Survey and Survey.Status==True:
            start = datetime.strptime(data['start_Date'], '%Y-%m-%d %H:%M:%S.%f')
            end = datetime.strptime(data['end_Date'], '%Y-%m-%d %H:%M:%S.%f')
            Survey.name = data['name']
            Survey.description = data['description']
            Survey.thank_you_message = data['thank_you_message']
            Survey.start_Date =start
            Survey.end_Date = end
            Survey.save_to_db()
            str1 =str(Survey.start_Date)
            str2 =str(Survey.end_Date)
            data ={
            "message":"survey updated",
            "id":Survey.id
            }

            return(data)

        else:
            return{"message":"no record found"}







# GETTING THE FULL LIST OF THE DATA
class surveyList(Resource):
    @jwt_required
    def get(self):
        data1=[]
        date=datetime.now()
        surveys = surveyModel.query.filter(surveyModel.end_Date >= date,  surveyModel.Status == True)
        # print('sss',survey)

        for x in surveys:

              data={
                    "id":x.id,
                    "name":x.name,
                    "description":x.description,
                    "thankYouMessage":x.thank_you_message,
                    "start_Date":str(x.start_Date),
                    "end_Date":str(x.end_Date)
                    }
              data1.append(data)

        print(data1)
        # s=data1 is None
        if data1 ==[]:
            print("sarath")
            return("no active survey")
        else:
            print("johan")
            return(data1)









        # for x in surveyModel:
        #     print(x)
        #






# str1=str(x.start_Date)
# str2 =str(x.end_Date)
# data ={
# "id":x.id,
# "name":x.name,
# "description":x.description,
# "thank_you_message":x.thank_you_message,
# "end_Date":str2,
# "start_Date":str1}
# survey.append(data)
# return(survey)











# POSTING THE DETAILS

class surveyData(Resource):

    @jwt_required
    def post(self):
        data = request.get_json()



        start = datetime.strptime(data['start_Date'], '%Y-%m-%d %H:%M:%S.%f')
        end = datetime.strptime(data['end_Date'], '%Y-%m-%d %H:%M:%S.%f')
        # print(type(start_Date))
        Survey = surveyModel(data['name'],data['description'],data['thank_you_message'],start,end)




        try:
            # print(Survey.end_Date)
            Survey.save_to_db()

        except:

            return {"message": "An error occurred inserting the item."}, 500

        str1=str(start)
        str2=str(end)
        data ={
        "message":"survey created",
        "id":Survey.id
        }

        return(data)
