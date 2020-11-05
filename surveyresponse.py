from db import db
from datetime import datetime



class surveyresponseModel(db.Model):
    __tablename__ = 'surveyresponse'

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id =db.Column(db.Integer, db.ForeignKey('question.id'))
    Status = db.Column(db.Boolean, default=True)
    start_date =db.Column(db.DateTime(80))
    end_date = db.Column(db.DateTime(80))
    option = db.Column(db.Integer, db.ForeignKey('options.id'))








    def __init__(self, survey_id,user_id,question_id,start_date,end_date,option):
        self.survey_id = survey_id
        self.user_id = user_id
        self.question_id = question_id
        self.start_date = start_date
        self.end_date = end_date
        self.option=option




    def json(self):
        return {'survey_id': self.survey_id,'user_id': self.user_id,'question_id': self.question_id,'start_date': self.start_date,'end_date':self.end_date,'id':self.id,'Status':self.Status,'option':self.option}

    @classmethod
    def find_by_id(cls,id):
        # print("sssssssssssss",cls.query.filter_by(id=id).first())
        return cls.query.filter_by(id=id).first()
    #

    @classmethod
    def find2_by_id(cls,survey_id):
        return cls.query.filter_by(survey_id=survey_id).all()

    @classmethod
    def find5_by_id(cls,user_id):
        return cls.query.filter_by(user_id=user_id).all()


    @classmethod
    def find3_by_id(cls,survey_id,user_id):
        return cls.query.filter_by(survey_id=survey_id,user_id=user_id).all()

    @classmethod
    def find4_by_id(cls,survey_id,question_id,user_id):
        return cls.query.filter_by(survey_id=survey_id,question_id=question_id,user_id=user_id).first()


    @classmethod
    def finds_by_id(cls,id):
        data= cls.query.filter_by(id=id).first()

        # print(data)
        # str1=str(data.start_date)
        # str2=str(data.end_date)
        data1={
        "survey_id":data.survey_id
        # "start_date":str1,
        # "end_date":str2,

        }
        return(data1)



    @classmethod
    def update_by_status(cls, id):
         data = cls.query.filter_by(id=id).first()
         data.Status=False
         db.session.commit()



    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
