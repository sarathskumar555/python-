from flask_restful import Resource, reqparse
from flask import Flask
from flask_jwt import jwt_required
from models.user import userModel
from models.department import departmentModel
from models.designation import designationModel
from flask import request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_refresh_token_required,get_jwt_identity
from flask_jwt_extended import jwt_required
from models.auditlog import auditlogModel
from models.role import roleModel
import re
import math
from email_validator import validate_email, EmailNotValidError

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

apps = Flask(__name__)
apps.config.from_object("config.Config")

#
# def refresh():
#     current_user = get_jwt_identity()
#     ret = {
#         'access_token': create_access_token(identity=current_user)
#     }



class user(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        # required=True,
                        # help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('mobilephone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('department_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('designation_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )

#  GETTING THE USER PROFILE  BY ID
    @jwt_required
    def get(self, id):
        user = userModel.find_by_id(id)
        # print(user)
        if user and user.Status==True:
            depart=user.department_id
            design=user.designation_id
            depart_data = departmentModel.find_by_id(depart)
            design_data = designationModel.find_by_id(design)
            if depart_data and design_data:
                res_depart =depart_data.json()
                res_design =design_data.json()
                user.department_id=res_depart
                user.designation_id=res_design
                return user.json()


        else:
            return{"message":"no record found"},404






# DELETING THE USERPROFILE BY ID

    @jwt_required
    def delete(self, id):
        user = userModel.find_by_id(id)
        data1=[]
        if user:
            if user.Status==True:
                user_data_del = userModel.update_by_status(id)
                data={
                "message":"record deleted",
                "id":user.id

                }
                data1.append(data)

                return (data1)


            else:
                return {'message': 'no record found.'}, 404

        else:
            return{"message":"no record found"},404

# UPDATING THE USERPROFILE BY ID
    @jwt_required
    def put(self,id):
        data = user.parser.parse_args()


        User = userModel.find_by_id(id)
        data1=[]
        if User and User.Status==True:
            # if userModel.find_by_name(data['username']):
            #     return {'message': "A user with name '{}' already exists.".format(data['username'])}, 400
            #
            #
            # if userModel.find_by_name(data['email']):
            #     return {'message': "A user with name '{}' already exists.".format(data['email'])}, 400
            if len(data['mobilephone'])==10 and data['mobilephone'].isdigit()==True:
                mobilephone1=data['mobilephone']
            else:
                return("invalid mobilephone")



            User.name = data['name']
            User.username = data['username']
            User.email = data['email']
            User.mobilephone = data['mobilephone']
            User.department_id = data['department_id']
            User.designation_id = data['designation_id']
            data={
            "message":"record upadated successfully",
            "id":User.id


            }
            User.save_to_db()
            data1.append(data)
            return(data1)

        else:
            return{"message":"no record found"},404








# GETTING THE FULL USERPROFILE LIST

class userList(Resource):
    @jwt_required
    def get(self):
         args = request.args
         if "page" in args and args.get("page")!='':
             page=int(args.get('page'))
             page = int(page-1)
         else:
             page =1
         if "per_page" in args and args.get("per_page")!='':
             per_page=int(args.get('per_page'))
         else:
             per_page=apps.config["PER_PAGE"]
         if "flag" in args and args.get("flag")=="active" or args.get("flag") =='':
             data=list(map(lambda x: x.json(), userModel.query.filter_by(Status=True).order_by(userModel.id.desc())))
             if data:
                  # print(data)
                  for i in data:
                      depart=i['department_id']
                      design=i['designation_id']
                      # print(depart)
                      dept_data = departmentModel.find_by_id(i['department_id'])
                      design_data = designationModel.find_by_id(i['designation_id'])
                      # print(dept_data)

                      if dept_data and design_data:
                          res_depart = dept_data.json()
                          # print(res_de)
                          res_design = design_data.json()
                          # print(res_design)
                          i['department_id']=res_depart
                          i['designation_id']=res_design
                  my_list = [data[i:i + per_page] for i in range(0, len(data), per_page)][page]
                  if page!=-1:
                      print("sarath")
                      length=len(data)
                      p=length/per_page
                      page_number=math.ceil(p)
                      return {"data": my_list,"maximum page=":page_number}
                  else:
                      return{"message":"page starts from 1"}
             else:
                  return{"message":"no record found"},404
             # if args.get("status") ==''and args.get("status")=="active":
             #     print("sarathssssssssssssssssssss")

         elif "flag" in args and  args.get("flag")=="inactive" :
             data=list(map(lambda x: x.json(), userModel.query.filter_by(Status=False).order_by(userModel.id.desc())))
             if data:
                  # print(data)
                  for i in data:
                      depart=i['department_id']
                      design=i['designation_id']
                      # print(depart)
                      dept_data = departmentModel.find_by_id(i['department_id'])
                      design_data = designationModel.find_by_id(i['designation_id'])
                      # print(dept_data)

                      if dept_data and design_data:
                          res_depart = dept_data.json()
                          # print(res_de)
                          res_design = design_data.json()
                          # print(res_design)
                          i['department_id']=res_depart
                          i['designation_id']=res_design
                  my_list = [data[i:i + per_page] for i in range(0, len(data), per_page)][page]
                  if page!=-1:
                      print("sarath")
                      length=len(data)
                      p=length/per_page
                      page_number=math.ceil(p)
                      return {"data": my_list,"maximum page=":page_number}
                  else:
                      return{"message":"page starts from 1"}
             else:
                  return{"message":"no record found"},404
             # if args.get("status") ==''or args.get("status")=="inactive":































class userData(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    # parser.add_argument('password',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be left blank!"
    #                     )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('mobilephone',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('department_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('designation_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
# POSTING THE DATA FOR USERPROFILE

    @jwt_required
    def post(self):
        data = userData.parser.parse_args()
        EMAIL=apps.config["EMAIL"]
        try:


            valid = validate_email(data['email'])
        except EmailNotValidError as e:
            return(str(e))
        p_data = bool(re.search(r"^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$", data['mobilephone']))
        if p_data == True:
            if userModel.find1_by_name(data['email']):
                return {'message': "A user with email '{}' already exists.".format(data['email'])}, 400

            if userModel.find_by_name(data['username']):
                return {'message': "A user with name '{}' already exists.".format(data['username'])}, 400
            password1 = userModel.get_random_string(8)
            role_id=2
            hashed_value=generate_password_hash(password1)
            User = userModel(data['name'],data['username'],hashed_value,data['email'],data['mobilephone'],data['department_id'],data['designation_id'],role_id)

            try:
                User.save_to_db()
            except:
                return {"message": "An error occurred inserting the item."}, 500


            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(apps.config["EMAIL"], apps.config["EMAIL_PASSWORD"])
            msg = MIMEMultipart()
            message = "Hello, Your username is : " + data['username'] + ". Your current password is : "+ password1 + ". You can change your password"
            msg['From'] = apps.config["EMAIL"]
            msg['To'] = data['email']
            msg['Subject'] = "Survey app password"
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
                        # s.sendmail("thomaschambilil@gmail.com", data['email'], message)
            s.quit()

            return {"message": "User created successfully & mail is send to ur account",'id':User.id}
        else:
            return {"message": "Enter valid phone no!!!"}

        # print('sssss',len(data['mobilephone']))


            # print("johan")













# API FOR LOGIN

class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = login.parser.parse_args()


        username= userModel.verify_by_username(data['username'])


        if username:
            result =(check_password_hash(username.password,data['password']))
            print(result)
            if result==True:
                if username.Status==True:
                    accesstoken=create_access_token(identity=username.id,fresh=True)
                    refreshtoken=create_refresh_token(username.id)
                    action="login"
                    page="home"
                    id=username.id
                    audit=auditlogModel(id,action,page)
                    try:
                        audit.save_to_db()
                    except:
                            return {"message": "An error occurred inserting the item."}, 500
                    userModel.tokenUpdate(username.id, accesstoken,refreshtoken)
                    role=roleModel.find_by_id(username.role_id)
                    role_type=role.name
                    data={
                    "accesstoken":accesstoken,
                    "refreshtoken":refreshtoken,
                    "message":"login succesfully",
                    "id":username.id,
                    "Status":username.Status,
                    "name":username.name,
                    "email":username.email,
                    "role":role_type


                    }
                    return data
                else:
                    return{"message":"No user found" }

            else:
                return {"message":"Incorrect password"},401

        else:
            return {"message":"Incorrect username"},401

# API FOR change PASSWORD
class change_Password(Resource):
    def post(self,id):
       data = request.get_json()
       min=apps.config["PASSWOR_MIN_LENGTH"]
       max=apps.config["PASSWOR_MAX_LENGTH"]
       SpecialSym=apps.config["SPECIAL_SYMBOL"]

       if len(data['new Password']) < min:

          return ('length should be at least 6')

       if len(data['new Password']) > max:

          return ('length should be not be greater than 12')

       if not any(char.isdigit() for char in data['new Password']):

          return ('Password should have at least one numeral')

       if not any(char.isupper() for char in data['new Password']):
          return ('Password should have at least one uppercase letter')

       if not any(char.islower() for char in data['new Password']):
          return ('Password should have at least one lowercase letter')

       if not any(char in SpecialSym for char in data['new Password']):
          return ('Password should have at least one of the symbols $@#%')

       current =userModel.find_by_id(id)
       if current:
           result =(check_password_hash(current.password,data['current Password']))
           print(result)
           if result==True:
               if data['new Password']== data['confirm Password']:
                   data['current Password']=data['new Password']
                   hashed_value=generate_password_hash(data['current Password'])
                   print(hashed_value)
                   userModel.change(id,hashed_value)
                   accesstoken=create_access_token(identity=current.id,fresh=True)
                   userModel.tokenUpdate1(id,accesstoken)
                   return {"message":"changed password successfully"}
               else:
                   return{"message":"unmatched passwords"},401
           else:
               return{"message":"unmatched current password"},401


       else:

            return{"message":"no record found"},404



class forgetPassword(Resource):


    def post(self):
        data = request.get_json()
        # print(data['enter the email'])
        forget=userModel.find1_by_name(data['enter the email'])
        if forget:
            userid=str(forget.id)
            token=forget.accesstoken

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(apps.config["EMAIL"], apps.config["EMAIL_PASSWORD"])
            msg = MIMEMultipart()
            message = " USERID: " + userid + ". TOKEN : "+ token
            msg['From'] = apps.config["EMAIL"]
            msg['To'] = data['enter the email']
            msg['Subject'] = "PASSWORD RESET"
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
            s.quit()
            return {"message":"details sent to the respective email address"}
        else:
            return{"message":"enter a valid email"}

class resetPassword(Resource):


    def post(self,user_id,accesstoken):
        data = request.get_json()
        min=apps.config["PASSWOR_MIN_LENGTH"]
        max=apps.config["PASSWOR_MAX_LENGTH"]
        SpecialSym=apps.config["SPECIAL_SYMBOL"]
        # user_id1=int(user_id)
        user=userModel.find_by_id(user_id)
        # print('ssssssssss',user)
        # token=userModel.find_by_token(accesstoken)
        if len(data['new Password']) < min:

           return ('length should be at least 6')

        if len(data['new Password']) > max:

           return ('length should be not be greater than 12')

        if not any(char.isdigit() for char in data['new Password']):

           return ('Password should have at least one numeral')

        if not any(char.isupper() for char in data['new Password']):
           return ('Password should have at least one uppercase letter')

        if not any(char.islower() for char in data['new Password']):
           return ('Password should have at least one lowercase letter')

        if not any(char in SpecialSym for char in data['new Password']):
           return ('Password should have at least one of the symbols $@#%')

        if user:
            if user.id==user_id and user.accesstoken==accesstoken :
                if data['new Password']==data['confirm Password']:
                    accesstoken=create_access_token(identity=user.id,fresh=True)
                    hashed_value=generate_password_hash(data['new Password'])
                    userModel.change(user_id,hashed_value)
                    userModel.tokenUpdate1(user_id,accesstoken)
                    return{"message":"password reset succesfully"}
                else:
                    return{"message":"unmatched reset and confirm password"}






            else:
                return{"message":"access denied"}
        else:
            return{"message":"access denied"}




class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):

        current_user = get_jwt_identity()
        print("sarathssssss",current_user)

        new_token = create_access_token(identity=current_user, fresh=False)
        userModel.tokenUpdate1(current_user,new_token)
        return {'access_token': new_token}, 200
