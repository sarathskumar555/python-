from db import db


class departmentModel(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    Status = db.Column(db.Boolean, default=True)
    user = db.relationship('userModel', backref='department', lazy=True)
    # designation_id = db.Column(db.Integer, db.ForeignKey('designation.id'))
    name = db.Column(db.String(30))





    def __init__(self, name):
        self.name = name


    def json(self):
        return {'name': self.name,'Status':self.Status,'id':self.id}


    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


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
