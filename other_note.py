import datetime
from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField,\
    EmbeddedDocumentField,EmbeddedDocument
from utils import require_arguments,success
from user import auth_by_token, User
from flask import request

#如何公开如同博客？
    
class Note_content(EmbeddedDocument):
    image_url = StringField()
    text = StringField()

class Other_note(Document):
    note_content = StringField()
    #note_content = EmbeddedDocumentField(Note_content)
    owner = ReferenceField(User,required=True)
    #title = StringField(required=True)
    note_category = StringField(required=True)

def note_add():
    [token,note_category,note_content]=require_arguments('token','note_category','note_content')
    user = auth_by_token(token)
    other_note = Other_note(owner=user,note_content=note_content).save()
    # if 'text' in request.form:
    #     text = request.form['text']
    #     note_content.text=text
    #     note_content.save()
    #     other_note.note_content=note_content
    #     other_note.save()
    # if 'image_url' in request.form:
    #     image_url = request.form['image_url']
    #     note_content.image_url=image_url
    #     note_content.save()
    #     other_note.note_content=note_content
    #     other_note.save()
    return {'status':'success'}

def note_by_id(id):
    other_note = Other_note.objects(id=id).first()
    if not Other_note:
        raise InvalidArgument('id does not exist')    
    # return success({'owner':assignment.owner,
    # 'scored problems':assignment.scored_problems,
    # 'students':assignment.students
    # })
    return other_note

def user_note():
    [token] = require_arguments('token')
    user = auth_by_token(token)
    #process = process.objects(owner_name=user.username).first()
    try:
        other_note = Other_note.objects.get(owner=user)
    except:
        other_note = None
    #     process_name = '学习'
    #     process_brief_intro = '复习所学内容'
    #     Process(owner=user,process_name=process_name,brief_intro=process_brief_intro).save()
    return success({'note_content':other_note.note_content,
            'process_brief_intro':process.brief_intro})


def note_edit():
    [token,note_id,note_content] = require_arguments('token','note_id','note_content')
    #这个错怎么处理
    user = auth_by_token(token)
    if not user:
        raise InvalidArgument('token required')
    other_note = note_by_id(note_id)
    other_note.note_content = note_content
    other_note.save()
    # if 'title' in request.form:
    #     title = request.form['title']
    #     other_note.title=title
    #     other_note.save()
    # if 'text' in request.form:
    #     text = request.form['text']
    #     note_content.text=text
    #     note_content.save()
    #     other_note.note_content=note_content
    #     other_note.save()
    # if 'image_url' in request.form:
    #     image_url = request.form['image_url']
    #     note_content.image_url=image_url
    #     note_content.save()
    #     other_note.note_content=note_content
    #     other_note.save()
    return {'status':'success'}



def note_delete():
    [token,note_id] = require_arguments('token','note_id')
    #需弹窗确认是否删除
    user = auth_by_token(token)
    if not user:
        raise InvalidArgument('token required')
    Other_note.objects(id=note_id).delete()
    return {'status':'success'}

