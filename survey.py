from db import db
from datetime import datetime



class surveyModel(db.Model):
    __tablename__ = 'survey'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    Status = db.Column(db.Boolean, default=True)
    thank_you_message = db.Column(db.String(80))
    start_Date =db.Column(db.DateTime(80))
    surveyquestion = db.relationship('surveyquestionModel', backref='survey', lazy=True)
    user = db.relationship('surveyresponseModel', backref='survey', lazy=True)
    end_Date = db.Column(db.DateTime(80))








    def __init__(self, name,description,thank_you_message,start_Date,end_Date):
        self.name = name
        self.description = description
        self.thank_you_message = thank_you_message
        self.start_Date = start_Date
        self.end_Date = end_Date
        print(type(self.start_Date))




    def json(self):
        return {'name': self.name,'description': self.description,'thank_you_message': self.thank_you_message,'start_Date': self.start_Date,'end_Date':self.end_Date,'id':self.id,'Status':self.Status}

    @classmethod
    def find_by_id(cls,id):
        # print("sssssssssssss",cls.query.filter_by(id=id).first())
        return cls.query.filter_by(id=id).first()
    @classmethod
    def find5_by_id(cls):
        return cls.query.all()



    #
    @classmethod
    def finds_by_id(cls,id):
        data= cls.query.filter_by(id=id).first()

        # print(data)
        # str1=str(data.start_Date)
        # str2=str(data.end_Date)
        data1={
        "id":data.id,
        "name":data.name,

        # "start_Date":str1,
        # "end_Date":str2,

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
