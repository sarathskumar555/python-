from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.auditlog import auditlogModel
from flask_jwt_extended import jwt_required
from models.user import userModel
from datetime import datetime
import time
from flask_paginate import Pagination, get_page_parameter
from flask import request
from verify_email import verify_email
import paginate
from flask import Flask
import math
apps = Flask(__name__)
apps.config.from_object("config.Config")
# # import python_paginate






# GETTING THE DETAILS BY NAME
class auditlog(Resource):
    @jwt_required
    def get(self,name):
        auditlog = auditlogModel.find1_by_id()
        user=userModel.find5_by_name(name)
        print(user)
        data1=[]
        if user:

            for x in auditlog:
                for y in user:
                    # print( y.user_id)
                    if str(x.user_id)==str(y.id):
                         time=str(x.created)
                         data={
                         "id":y.id,
                         "employee name":y.name,
                          "page":x.page,
                          "action":x.action,
                           "timestamp":time
                           }
                         data1.append(data)
            return(data1)




        else:
            return{"message":"No audit log found"}


# # GETTING THE FULL DETAILS
# class auditlogList(Resource):
#     @jwt_required
#     def get(self):
#         audit=[]
#         for x in auditlogModel.query.filter_by(Status=True):
#             user =userModel.find_by_id(x.user_id)
#             time=str(x.created)
#             data={
#             "id":user.id,
#             "employee name":user.name,
#             "page":x.page,
#             "action":x.action,
#             "timestamp":time
#             }
#             audit.append(data)
#         return(audit)
#
#
class auditlogData(Resource):
    # @jwt_required
    def get(self):
        audit=[]
        args = request.args
        search = request.args
        s_final = search.to_dict()
        # page = int(s_final['page'])
        # page = page-1
        # print(page)

        # per_page = 5
        startdatess = datetime.strptime('2020-09-12 04:30:35.306285','%Y-%m-%d %H:%M:%S.%f')
        print(startdatess, datetime.now())
        if "startDate" in args and args.get("startDate") !='':
          startdates = datetime.strptime(args.get("startDate"), '%Y-%m-%d %H:%M:%S.%f')
        else:
            startdates = datetime.strptime('2020-09-12 04:30:35.306285','%Y-%m-%d %H:%M:%S.%f')
        if "endDate" in args and args.get("endDate") !='':
         enddates = datetime.strptime(args.get("endDate"), '%Y-%m-%d %H:%M:%S.%f')
        else:
            enddates = datetime.now()
            print(enddates)
        if "page" in args and args.get("page")!='':
            page = int(s_final['page'])
            page = int(page-1)
        else:
            page=1
            # page = page-1
        if "per_page" in args and args.get("per_page")!='':
            per_page=int(args.get('per_page'))
        else:
            per_page=apps.config["PER_PAGE"]
        for x in auditlogModel.query.filter(auditlogModel.created >= startdates, auditlogModel.created <= enddates):
            user =userModel.find_by_id(x.user_id)
            time=str(x.created)
            data={
            "username":user.username,
            "page":x.page,
            "action":x.action,
            "timestamp":time,
            # "sourceIp":x.sourceIp
            }
            audit.append(data)

        if audit==[]:
           return{"message":"no record found"}, 404
        else:
            if page!=-1:
                print("222",len(audit))
                length=len(audit)
                p=length/per_page
                l=math.ceil(p)
                my_list = [audit[i:i + per_page] for i in range(0, len(audit), per_page)][page]
                return {"data": my_list,"maximum page":l}
            else:
                return{"message":"page starts from 1"}

    # @jwt_required
    # def get(self):
    #     # print(dir(Pagination))
    #     data1=[]
    #     args = request.args
    #     if "startDate" in args and args.get("startDate") !='':
    #       startDates = datetime.strptime(args.get("startDate"), '%Y-%m-%d %H:%M:%S.%f')
    #     else:
    #         startDates = datetime.strptime('2019-10-09 00:00:00.000000','%Y-%m-%d %H:%M:%S.%f')
    #     if "endDate" in args and args.get("endDate") !='':
    #      endDates = datetime.strptime(args.get("endDate"), '%Y-%m-%d %H:%M:%S.%f')
    #     else:
    #         endDates = datetime.now()
    #     if "page" in args and args.get("page")!='':
    #         page=int(args.get('page'))
    #         page = int(page-1)
    #     else:
    #         page =1
    #     if "per_page" in args and args.get("per_page")!='':
    #         per_page=int(args.get('per_page'))
    #     else:
    #         per_page=2
    #
    #     # result=auditlogModel.query.filter(auditlogModel.created <= endDates, auditlogModel.created >= startDates)
    #     # print(result)
    #
    #
    #
    #     for x in auditlogModel.query.filter(auditlogModel.created <= endDates, auditlogModel.created >= startDates):
    #         user =userModel.find_by_id(x.user_id)
    #         time=str(x.created)
    #         data={
    #         "employee Name":user.username,
    #         "page":x.page,
    #         "action":x.action,
    #         "timestamp":time,
    #
    #         }
    #         data1.append(data)
    #     my_list = [data1[i:i + per_page] for i in range(0, len(data1), per_page)][page]
    #
    #     if data1!=[]:
    #         # print("johan")
    #         # print("rojan",page)
    #         if page!=-1:
    #             print("sarath")
    #             length=len(data1)
    #             p=length/per_page
    #             page_number=math.ceil(p)
    #             return {"data": my_list,"maximum page=":page_number}
    #         else:
    #             return{"message":"page starts from 1"}
    #
    #
    #
    #
    #     else:
    #         return{"message":"no audit log found"}

















        #
        # if data1!=[]:
        #     length=len(data1)
        #     p=length/per_page
        #     page_number=math.ceil(p)
        #     print("page",page)
        #     print("page_number",page_number)
        #     page=page-1
        #     print("rojan",page)
        #     if per_page%2!=0:
        #         if page<page_number and page!=-1:
        #
        #
        #             my_list = [data1[i:i + per_page] for i in range(0, len(data1), per_page)][page]
        #             print("leng",len(my_list))
        #             return {"data": my_list}
        #         else:
        #             return{"message":"page number out of index","maximum page":page_number-1}
        #     else:
        #         # page=page-1
        #         print("rojan",page)
        #         if page<=page_number and page!=-1:
        #
        #
        #             my_list = [data1[i:i + per_page] for i in range(0, len(data1), per_page)][page]
        #             print("leng",len(my_list))
        #             return {"data": my_list}
        #         else:
        #             return{"message":"page number out of index","maximum page":page_number}
        #
        #
        #
        #
        #
        #
        # else:
        #     return{"message":"no audit log found"}
