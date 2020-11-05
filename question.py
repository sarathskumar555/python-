from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.question import questionModel
from models.surveyquestion import surveyquestionModel
from models.options import optionsModel
from flask_jwt_extended import jwt_required
from flask import request




class question(Resource):
    # GETTING THE  DETAILS BY ID
    @jwt_required
    def get(self, id):
        # print(id)
        question_data = questionModel.find_by_id(id)
        options_data = list(map(lambda x: x.json(), optionsModel.query.filter_by(Status=True,question_id=id)))
        li = []
        if question_data and options_data:
            if question_data.Status == True:
                # print(len(options_data))
                for i in range(len(options_data)):
                    op = options_data[i]['options']
                    op1=options_data[i]['id']
                    print(op1)
                    data3={
                    "id":op1,"option":op
                    }
                    li.append(data3)
                    # print(li)
                question_list = question_data.json()

                data = {
                    "id":question_list['id'],
                    "question":question_list['description'],
                    "options":li,
                    "Status":question_list['Status']
                }
                # print(data)
                return data
        return {'message': 'not found'}, 404


        # question = questionModel.find_by_id(id)
        # if question and question. Status==True:
        #     str2=(question.options).split(",")
        #     data={
        #     "id":question.id,
        #     "description":question.description,
        #     "options":str2,
        #     "Status":question.Status
        #     }
        #     return(data)
        # else:
        #     return{"message":"no record found"},404








# DELETING THE DETAILS BY ID
    @jwt_required
    def delete(self, id):
        question_data = questionModel.find_by_id(id)
        print(question_data.json())
        if question_data and question_data.Status == True:

            question_data = questionModel.update_by_status(id)
            sur_data=surveyquestionModel.update2_by_status(id)
            sur_que_data = list(map(lambda x: x.json(), optionsModel.find_by_qid(id)))

            for x in sur_que_data:
                print(x['question_id'])
                if x['Status'] == True:

                    s_del_data = optionsModel.update_by_status(x['id'],x['question_id'])

            return {'id': id, 'message': 'deleted.'}
        return {'message': 'not found.'}, 404
        # question = questionModel.find_by_id(id)
        # print(id)
        # if question and question.Status==True:
        #     survey =surveyquestionModel.query.all()
        #     for x in survey:
        #         if x.question_id==question.id:
        #             surveyquestionModel.update_by_status(x.survey_id,x.question_id)
        #     user_data_del = questionModel.update_by_status(id)
        #     str2=(question.options).split(",")
        #
        #     data={
        #     "message":"record deleted",
        #     "id":question.id
        #
        #      }
        #     return (data)
        # else:
        #      return{"message":"no record found"},404









        #
        #     user_data_del = questionModel.update_by_status(id)
        #     str2=(question.options).split(",")
        #
        #     data={
        #     "message":"record deleted",
        #     "id":question.id,
        #     "description":question.description,
        #     "options":str2
        #     }
        #     return (data)
        #
        #
        # else:
        #     return{"message":"no record found"},404


# UPDATING THE DETAILS BY ID
    @jwt_required
    def put(self,id):
            data =request.get_json()
            # print(data)
            question_data = questionModel.find_by_id(id)
            if question_data and question_data.Status == True:
                question_data.question = data['description']
                question_data.save_to_db()

            options = data['options']

            option_data = list(map(lambda x: x.json(), optionsModel.query.filter_by(Status=True, question_id=id)))
            print(len(option_data))
            if option_data:
                li = []
                for k in option_data:
                    li.append(k['id'])
                print(len(li))
                if len(options) == len(li):
                    for i in range(len(options)):
                        # print("hh",li[i])
                        # print("f",li[i],options[i])
                        optionsModel.optionUpdate(li[i],options[i])
                else:
                    return("error") ,404
            else:
                return {'message': 'not found.'}, 404

            return {"message": "Updated successfully!!!"}, 201


                            # "data":data


                        # print("hh",li[i])
                        # print("f",li[i],options[i])






        # data=request.get_json()
        # question = questionModel.find_by_id(id)
        # op1=optionsModel.find_by_id1(id)
        # print(op1)
        # if question and question.Status==True:
        #     question.description=data['description']
        #     question_set.save_to_db()
        #     data = question_set.json()
        #     options = data['options']
        #     print(data['options'][0])
        #     # if len(op1)==len(options):
        #     for i in op1:
        #         x=0
        #         i.option=data['options'][x]
        #         x=x+1




















        # data = request.get_json()
        #
        # question = questionModel.find_by_id(id)
        #
        # if question and question.Status==True:
        #     str1 = ','.join(data['options'])
        #
        #     question.description = data['description']
        #     question.options=str1
        #
        #     question.save_to_db()
        #     str2=(question.options).split(",")
        #     data={
        #     "message":"record updated",
        #     "id":question.id
        #
        #         }
        #     return (data)
        #
        #
        #     return question.json()
        # else:
        #     return{"message":"no record found"},404
        #






# GETTING THE FULL LIST OF THE DETAILS

class questionList(Resource):
    @jwt_required
    def get(self):
        status = True
        final = []
        questions = list(map(lambda x: x.json(), questionModel.query.filter_by(Status=status)))
        print(questions)
        for s in questions:
            o_data = list(map(lambda x: x.json(), optionsModel.query.filter_by(Status=True, question_id=s['id'])))
            print(o_data)
            li = []
            if o_data:
                print(len(o_data))
                for i in range(len(o_data)):
                    op = o_data[i]['options']
                    op1=o_data[i]['id']
                    data3={
                    "id":op1,"option":op
                    }
                    print(op)
                    li.append(data3)
                    print(li)
                    # q_li = questions
                last = {
                        "id": s['id'],
                        "question": s['description'],
                        "options": li,
                        "Status": s['Status'],
                    }
                print(last)
                final.append(last)
                    # return last
        return {'Question_list': final}

        # question=[]
        # for x in questionModel.query.filter_by(Status=True):
        #     str2=(x.options).split(",")
        #     data={
        #
        #     "id":x.id,
        #     "description":x.description,
        #     "options":str2
        #         }
        #     question.append(data)
        #
        #
        # return question












# POSTING THE DETAILS

class questionData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('options',
                        type=str,
                        action='append',
                        required=True,
                        help="This field cannot be blank."
                        )
    @jwt_required
    def post(self):
        data = questionData.parser.parse_args()
        options = data['options']
        # print(data)
        # print("oo",options)
        # print(len(options))

        if questionModel.find_by_description(data['description']):
            return {"message": "Already exists"}, 400
        try:
            question_set = questionModel(data['description'])
            question_set.save_to_db()
            data = question_set.json()
            # print(data)
            for i in range(len(options)):
                # print("kkk", options[i])
                option_set = optionsModel(options[i],data['id'] )
                option_set.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {"message": "created successfully!!!",
                # "data":data
                }, 201


class Options(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('options',
                        type=str,
                        action='append',
                        required=True,
                        help="This field cannot be blank."
                        )
    @jwt_required
    def put(self,id):
        data = Options.parser.parse_args()
        options = data['options']
        q1= optionsModel.find_by_id1(id)
        q2=questionModel.find_by_id(id)
        # for i in range(len(options)):
        #         print("kkk", options[i])
        #
        # if optionsModel.find_by_option(options[i]) and id==x.question_id:
        #     return {"message": "Already exists"}, 400
        try:

            for i in range(len(options)):
                # print("kkk", options[i])
                option_set = optionsModel( options[i],id)
                option_set.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return {"message": "inserted successfully"
                # "data":data
                }, 201





























        # print(data1)

        # return {"message": "department created successfully ",'id':Department.id} , 201


    #
    # @jwt_required
    # def post(self):
    #     data=request.get_json()
    #     # if departmentModel.find_by_name(data['name']):
    #     #     return {'message': "A department with name '{}' already exists.".format(data['name'])}, 400
    #
    #     str1 = ','.join(data['options'])
    #
    #     question = questionModel(data['description'],str1)
    #
    #
    #     try:
    #         question.save_to_db()
    #     except:
    #         return {"message": "An error occurred inserting the item."}, 500
    #
    #
    #
    #     str2=str1.split(",")
    #     # print(str2[5])
    #     data={
    #     "message":"record created",
    #     "id":question.id
    #
    #     }
    #     return(data)






class OptionsRemove(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('options',
                        type=str,
                        action='append',
                        required=True,
                        help="This field cannot be blank."
                        )
    @jwt_required
    def delete(self, id,question_id):
        q_data = optionsModel.find_by_options1(id,question_id)
        print(q_data)
        if q_data and q_data.Status == True:
            print("222")
            q_data = optionsModel.update_by_status(id,question_id)


            return {'id': id, 'message': 'deleted.'}
        return {'message': 'not found.'}, 404
