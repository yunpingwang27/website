import datetime
from flask import Flask, request
from flask_mongoengine import MongoEngine
from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, ListField, EmbeddedDocument, \
    EmbeddedDocumentListField,EmbeddedDocumentField

from user import auth_by_token, User
from utils import require_arguments, success

class Event(Document):
    event_time = DateTimeField()
    event_name = StringField(required=True)
    event_type = StringField(required=True,regex='(work|study|rest|others)')
    owner = ReferenceField(User,required=True)
    
def add_event():
    [token,event_name,event_type]=require_arguments('token','event_name','event_type')
    user = auth_by_token(token)
    #problem = Problem(problem=problem,key=key,type_=type_,owner=user,difficulty=difficulty).save()
    event = Event(event_name=event_name,event_type=event_type,owner=user).save()
    return success({'id':str(event.id)})

def event_by_id(id):
    event = Event.objects(id=id).first()
    if not event:
        raise InvalidArgument('id does not exist')
    return event 

def edit_event():
    [token,id,event_name,event_type]=require_arguments('token','id','event_name','event_type')
    user = auth_by_token(token)
    event = event_by_id(id)
    event.event_name=event_name
    event.event_type=event_type
    event.save()
    return {'status':'success'}

def get_user_event():
    [token] = require_arguments('token')
    user = auth_by_token(token)
    #event = Event.objects(owner_name=user.username).first()
    event = Event.objects.get(owner=user)
    return success({'event_name':event.event_name,
                    'event_type':event.event_type})
