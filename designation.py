from db import db


class designationModel(db.Model):
    __tablename__ = 'designation'

    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('userModel', backref='designation', lazy=True)
    Status = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(30))




    def __init__(self, name):
        self.name = name


    def json(self):
        return {'name': self.name,'Status':self.Status,'id':self.id}

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

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
