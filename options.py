from db import db


class optionsModel(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, default=True)
    options =db.Column(db.String(80))
    question_id =db.Column(db.Integer, db.ForeignKey('question.id'))
    options1 = db.relationship('surveyresponseModel', backref='options', lazy=True)


    def __init__(self,options,question_id):
        self.question_id =question_id
        self.options =options

    def json(self):
        # options = self.options.split(",")
        return {'id':self.id, 'question_id':self.question_id,'options': self.options,'Status':self.Status}




    def save_to_db(self):

        db.session.add(self)

        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_qid(cls, qid):
        return cls.query.filter_by(question_id=qid)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_id1(cls, _id):
        return cls.query.filter_by(question_id=_id).all()

    @classmethod
    def optionUpdate(cls, id, options):
        data = cls.query.filter_by(id=id).first()
        data.options = options

        db.session.commit()

    @classmethod
    def find_by_option(cls, options):
        return cls.query.filter_by(options=options).first()

    @classmethod
    def find_by_options1(cls, id,question_id):
        return cls.query.filter_by(question_id=question_id,id=id).first()





    @classmethod
    def update_by_status(cls, id,q_id):
        data = cls.query.filter_by(id=id,question_id=q_id).first()
        print(data)
        data.Status=False
        db.session.commit()
        return cls.query.filter_by(id=id).first()

    @classmethod
    def full_get(cls,username):
        data = cls.query.filter_by(username=username).first()
        print(data)
