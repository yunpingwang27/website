import datetime
from flask import Flask, request
from flask_mongoengine import MongoEngine
from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, ListField, EmbeddedDocument, \
    EmbeddedDocumentListField,EmbeddedDocumentField

from user import auth_by_token, User
from utils import require_arguments, success

#在线时长作为用户属性之一？
#考试/做题规定时间用倒计时


# class Learn_time(Document):
#     owner = ReferenceField(User,required=True)
#     time_length = DateTimeField(required=True)

def record_time(record,token):
    #五秒一次
    flag = False
    try:
        user = auth_by_token(token)
        flag = True
        record = record + 5
    #InvalidArgument()？
    except InvalidArgument:
        flag = False
    return {'user':user,'record_time':record,
    'condition':flag}

def week_time(t):
    now = datetime.datetime.now()
    due = t + datetime.timedelta(days=7)
    if now > due:
        t = now
        return True
    return False
        #return record_time(record)#未成

def week_report():
    
    
    

# def get_time(token):
#     user = auth_by_token(token)
#     learn_time = Learn_time.objects(owner=user).first()
#     #time_length=
#     learn_time.time_length=time_length
#     learn_time.save()
#     if datetime.datetime.now()>learn_time.time_length:
#         return False
#     return token.user