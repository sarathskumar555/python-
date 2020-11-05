from db import db
from datetime import datetime


class auditlogModel(db.Model):
    __tablename__ = 'auditlog'

    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, default=True)
    # user = db.relationship('userModel', backref='department', lazy=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    created = db.Column(db.DateTime, nullable=False,default=datetime.now())
    action= db.Column(db.String(80))
    page = db.Column(db.String(80))
    # user_id = db.Column(db.String(80))



    def __init__(self,user_id,action,page):
        # self.created:created
        self.action = action
        self.page=page
        self.user_id=user_id


    def json(self):
        return {'action':self.action,'page':self.page,'Status':self.Status,'id':self.id}


    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find1_by_id(cls):
        return cls.query.all()


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
