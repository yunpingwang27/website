import datetime
from flask import Flask, request
from flask_mongoengine import MongoEngine
from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, ListField, EmbeddedDocument, \
    EmbeddedDocumentListField,EmbeddedDocumentField
from user import auth_by_token, User
from utils import require_arguments, success

class Process(Document):
    owner = ReferenceField(User,required=True)
    process_name = StringField(required=True)
    book = StringField()
    section = StringField()
    brief_intro = StringField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    
def add_process():
    [token,process_name,book,section,brief_intro]=require_arguments('token','process_name','book','section','brief_intro')
    user = auth_by_token(token)
    #problem = Problem(problem=problem,key=key,type_=type_,owner=user,difficulty=difficulty).save()
    process = Process(owner=user,process_name=process_name,book=book,section=section,brief_intro=brief_intro).save()
    return success({'id':str(process.id)})

def process_by_id(id):
    try:
        process = Process.objects.get(id=id)
    except:
        process = None
        # process_name = '学习'
        # process_brief_intro = '复习所学内容'
        # Process(owner=user,process_name=process_name,process_brief_intro=process_brief_intro).save()
    if not process:
        raise InvalidArgument('id does not exist')
    return process 

def edit_process():
    [token,id,process_name,book,section,brief_intro]=require_arguments('token','id','process_name','book','section','brief_intro')
    user = auth_by_token(toketn)
    process = process_by_id(id)
    process.process_name = process_name
    process.book = book
    process.section = section
    process.brief_intro = brief_intro
    process.save()
    return {'status':'success'}

def user_process():
    [token] = require_arguments('token')
    user = auth_by_token(token)
    #process = process.objects(owner_name=user.username).first()
    if Process.objects(owner=user).count()>0:
        processes = Process.objects(owner=user).all()
        # return success({'process_name':processes.process_name,'process_brief_intro':processes.brief_intro})          
        return success([{'process_name':process.process_name,'process_brief_intro':process.brief_intro} for process in processes])
    else:
        process_name = '学习'
        process_brief_intro = '学习永无止境'
        Process(owner=user,process_name=process_name,brief_intro=process_brief_intro).save()
        processes = Process.objects.get(owner=user).all()
        return success([{'process_name':process.process_name,'process_brief_intro':process.brief_intro} for process in processes])


def delete_process():
    [token,id] = require_arguments('token','id')
    user = auth_by_token(token)
    Process.objects(id=id).delete()
    return {'status':'success'}