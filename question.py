from db import db


class questionModel(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(80))
    # options =db.Column(db.String(80))
    surveyquestion = db.relationship('surveyquestionModel', backref='question', lazy=True)
    user = db.relationship('surveyresponseModel', backref='question', lazy=True)
    options = db.relationship('optionsModel', backref='question', lazy=True)
    # user = db.relationship('userModel', backref='department', lazy=True)
    # designation_id = db.Column(db.Integer, db.ForeignKey('designation.id'))






    def __init__(self,description):
        self.description =description
        # self.options =options


    def json(self):
        return {'id':self.id,'Status':self.Status,'description':self.description}


    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_id10(cls,id):
        return cls.query.filter_by(id=id).all()

    @classmethod
    def find_by_description(cls,description):
        return cls.query.filter_by(description=description).first()



    @classmethod
    def find3_by_id(cls):
        return cls.query.all()


    @classmethod
    def update_by_status(cls, id):
         data = cls.query.filter_by(id=id).first()
         data.Status=False
         db.session.commit()

    def save_to_db(self):

        db.session.add(self)

        db.session.commit()
        # print("success",data)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
