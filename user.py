from db import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
import random
import string


class userModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    username = db.Column(db.String(80))
    password = db.Column(db.String(128))
    email = db.Column(db.String(255))
    mobilephone = db.Column(db.String(15))
    created = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    Status = db.Column(db.Boolean, default=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    designation_id = db.Column(db.Integer, db.ForeignKey('designation.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    accesstoken = db.Column(db.String(255),nullable=False,default='')
    refreshtoken = db.Column(db.String(255),nullable=False,default='')
    user = db.relationship('surveyresponseModel', backref='user', lazy=True)
    user2 = db.relationship('auditlogModel', backref='user', lazy=True)




    def __init__(self, name,username,password,email,mobilephone,department_id,designation_id,role_id):
        self.name = name
        self.username = username
        self.password = password
        self.email = email
        self.mobilephone = mobilephone
        self.department_id = department_id
        self.designation_id = designation_id
        self.role_id=role_id


    def json(self):
        return {'name': self.name,'username': self.username,'email': self.email,'mobilephone': self.mobilephone,'department_id': self.department_id,'designation_id': self.designation_id,'id':self.id,'Status':self.Status}

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find5_by_name(cls,name):
        return cls.query.filter_by(name=name).all()


    @classmethod
    def find2_by_id(cls):
        return cls.query.all()

    @classmethod
    def find1_by_name(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_name(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def verify_by_password(cls,password):
        # data=cls.query.filter_by(password=password).first()
        return cls.query.filter_by(password=password).first()

    @classmethod
    def verify_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def update_by_status(cls, id):
         data = cls.query.filter_by(id=id).first()
         data.Status=False
         db.session.commit()

    @classmethod
    def change(cls, id,hashed_value):
         data = cls.query.filter_by(id=id).first()
         data.password=hashed_value

         db.session.commit()

    @classmethod
    def reset(cls, user_id,hashed_value):
         data = cls.query.filter_by(id=user_id).first()
         data.password=hashed_value

         db.session.commit()


    @classmethod
    def tokenUpdate(cls, id, access_token,refresh_token):
        data = cls.query.filter_by(id=id).first()
        data.accesstoken = access_token
        data.refreshtoken = refresh_token
        db.session.commit()


    @classmethod
    def tokenUpdate1(cls, id, access_token):
        data = cls.query.filter_by(id=id).first()
        data.accesstoken = access_token

        db.session.commit()

    @classmethod
    def find_by_token(cls, accesstoken):
        return cls.query.filter_by(accesstoken=accesstoken).first()

    @classmethod
    def get_random_string(cls,length):
        # Random string with the combination of lower and upper case
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        print("Random string is:", result_str)
        return result_str





    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
