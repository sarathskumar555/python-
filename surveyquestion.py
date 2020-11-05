from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.surveyquestion import surveyquestionModel
from flask_jwt_extended import jwt_required
from flask import request,jsonify
from models.survey import surveyModel
from models.question import questionModel
from models.options import optionsModel
from flask_jwt_extended import jwt_required

class surveyquestion(Resource):
        # @jwt_required
        def get(self,id):
            status = True
            # args = request.args
            # if "Status" in args and args.get("Status") != '':
            #
            #     status = args.get("Status")
            sur_que_data = list(map(lambda x: x.json(), surveyquestionModel.query.filter_by(survey_id=id,Status = status).order_by(surveyquestionModel.id)))


            if sur_que_data !=[] :


                s_data = surveyModel.find_by_id(id)
                data = {
                        "id": s_data.id,
                        "name": s_data.name,

                    }
                su_list = []
                for s in sur_que_data:
                    q_list = s['question_id']
                    # print("id",q_list)
                    q_data = questionModel.find_by_id(s['question_id'])
                    # que_res_data = q_data.json()
                    # print(que_res_data)

                    o_data = list(map(lambda x: x.json(), optionsModel.query.filter_by(Status=True, question_id=s['question_id'])))
                    li = []
                    if q_data and o_data:
                        if q_data.Status == True:
                            # print(len(o_data))
                            for i in range(len(o_data)):
                                op1 = o_data[i]['options']
                                op2 = o_data[i]['id']
                                print("ssssssssssss",op1)
                                data3={
                                "id":op2,"option":op1
                                }
                                li.append(data3)
                                # print(li)
                            q_li = q_data.json()

                            data1 = {
                                "id": q_li['id'],
                                "question": q_li['description'],
                                "options": li,
                                "Status": q_li['Status'],
                            }
                        # Survey_question_list = {
                        # # "surveyid":data,
                        #     "questions":data1
                        #     # "order":s['order']
                        #     }

                        su_list.append(data1)



                last = {
                        "survey":data,
                        "question data":su_list
                    }

                return ( last)

            if sur_que_data == []:
                # print("www")
                return {"message": "No survey found!!!"}
    # def get(self, survey_id):
    #         surveyque = list(map(lambda x: x.json(), surveyquestionModel.query.filter_by(survey_id=survey_id)))
    #
    #         s_data = surveyModel.find_by_id(survey_id)
    #         data = {
    #             "survey_id": s_data.id,
    #             "name": s_data.name,
    #
    #         }
    #         data = []
    #         for s in surveyque:
    #             q_data = questionModel.find_by_id(s['question_id'])
    #             que = q_data.json()
    #             queustion_list = {
    #             "question_data":que,
    #
    #             }
    #
    #             data.append(queustion_list)
    #
    #         data1 = {
    #             "survey_data":data,
    #             "questions":data
    #         }
    #
    #         return {'queustion_list': data1}












# GETTING THE DETAILS BY SURVEYID
    # @jwt_required
    # def get(self,survey_id):
    #     surveyQuestion = surveyquestionModel.find_by_id(survey_id)
    #     # print(surveyQuestion)
    #
    #
    #     data = []
    #     if surveyQuestion:
    #         for x in surveyQuestion:
    #             # print(x)
    #             if x and x.Status==True:
    #
    #                 # surveyid=x.survey_id
    #                 questionid=x.question_id
    #                 # surveydata=surveyModel.finds_by_id(surveyid)
    #                 questiondata=questionModel.find_by_id(questionid)
    #                 surveydata=surveyModel.finds_by_id(survey_id)
    #                 # print(surveydata.id)
    #                 if surveydata and questiondata:
    #                     str2=(questiondata.options).split(",")
    #                     data2={
    #                     "id":questiondata.id,
    #                     "description":questiondata.description,
    #                     "options":str2
    #                     }
    #                     data3={
    #                     "id":surveydata['id'],
    #                     "name":surveydata['name']
    #                     }
    #
    #
    #
    #                     # res_que =questiondata.json()
    #                     # print(res_que)
    #                     data1 = {
    #                     "survey_id":data3,
    #                     "question_id":data2}
    #                     data.append(data1)
    #             else:
    #                 return{"message":"no record found"}
    #
    #
    #
    #         return(data)
    #     else:
    #         return{"message":"no record found"}








# DELETING THE SURVEY FULL USING THE SURVEYID

    # @jwt_required
    # def delete(self, survey_id):
    #     surveyQuestion = surveyquestionModel.find_by_id(survey_id)
    #     print(surveyQuestion)
    #
    #     for x in surveyQuestion:
    #         if x:
    #             x.delete_from_db()
    #         else:
    #             return("no record found")
    #     else:
    #         return("record deleted")







# UPDATING THE QUESTION USING THE SURVEYID ,QUESTIONID

class surveyquestionList(Resource):

    # @jwt_required
    @jwt_required
    def put(self, survey_id,question_id):

        data = request.get_json()
        survey = surveyquestionModel.finds_by_id(survey_id,question_id)
        if survey and survey.Status == True:
            survey.survey_id = data['survey_id']
            survey.question_id = data['question_id']
            # survey.order = data['order']
            survey.save_to_db()
            return{'message': 'Survey updated.','id':survey.id} ,200
        else:
            return {'message': 'Survey not found.'}, 400


    def delete(self, survey_id,question_id):
            survey = surveyquestionModel.finds_by_id(survey_id,question_id)
            if survey and survey.Status == True:
                survey_del = surveyquestionModel.update_by_status(survey_id,question_id)
                # print(survey_del)
                return {'message': 'survey deleted.','id':survey.id}
            else:
                return {'message': 'survey not found.'}, 404












# POSTING THE DETAILS
class surveyquestionData(Resource):

    #
    @jwt_required
    def post(self):
        data =request.get_json()
        if surveyquestionModel.finds_by_id(data['survey_id'],data['question_id']):
            return {"message": "Already exists"}, 400





        surveyQuestion = surveyquestionModel(**data)


        try:
            surveyQuestion.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {"message": "surveyquestion created successfully ",'id':surveyQuestion.id} , 201
