from db import db


class surveyquestionModel(db.Model):
    __tablename__ = 'survey Question'

    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, default=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    # order = db.Column(db.Integer,autoincrement=True)







    def __init__(self,survey_id,question_id):
        self.survey_id =survey_id
        self.question_id = question_id
        # self.order=order
        #

    def json(self):
        return {'survey_id': self.survey_id,'question_id':self.question_id,'Status':self.Status,'id':self.id}

    #
    # @classmethod
    # def find_by_name(cls,name):
    #     return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,survey_id):
        return cls.query.filter_by(survey_id=survey_id).all()

    @classmethod
    def finds_by_id(cls,survey_id,question_id):

      return cls.query.filter_by(question_id= question_id,survey_id= survey_id ).first()



    @classmethod
    def update_by_status(cls,survey_id,question_id):
        data = cls.query.filter_by(question_id= question_id,survey_id= survey_id ).first()
        print(data)
        data.Status=0
        db.session.commit()
        return cls.query.filter_by(question_id= question_id,survey_id= survey_id ).first()

    @classmethod
    def update1_by_status(cls,id):
        data = cls.query.filter_by(survey_id= id ).first()
        # print(data.Status)
        data.Status=0
        db.session.commit()

    @classmethod
    def update2_by_status(cls,id):
        data = cls.query.filter_by(question_id= id ).all()
        print(data)
        for x in data:
            x.Status=0
            db.session.commit()

        # print(data.Status)
        # data.Status=0
        # db.session.commit()
        # return cls.query.filter_by(question_id= question_id,survey_id= survey_id ).first()


    # @classmethod
    # def update_by_status(cls, id):
    #      data = cls.query.filter_by(id=id).first()
    #      data.Status=False
    #      db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
