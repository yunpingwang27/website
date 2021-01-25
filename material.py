import datetime
from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField,\
    EmbeddedDocumentField,EmbeddedDocument
from utils import require_arguments,success
from user import auth_by_token, User
from flask import request
def material_add():
    #  验证登陆
    token = request.form.get("token")
    if not token:
        return {"status": "failed", "data": "token required"}
    user = auth_by_token(token)
    if not user:
        return {"status": "failed", "data": "invalid token"}

    if 'title' in request.form:
        title = request.form['title']
    else:
        return {"status": "failed", "data": "title required"}
    if 'content' in request.form:
        content = request.form['content']
    else:
        return                                                                                                                                {"status": "failed", "data": "content required"}
    if 'category' in request.form:
        category = request.form['category']
    else:
        return {"status": "failed", "data": "category required"}

    if user.type not in ['teacher', 'student']:
        return {"status": "failed", "data": "invalid user type"}
    if user.type == "teacher" and category not in ['经典教案', '网课视频', '笔记展示']:
        return {"status": "failed", "data": "category invalid"}
    if user.type == "student" and category != '笔记展示':
        return {"status": "failed", "data": "category invalid"}

    mat = Material(content=content, title=title, category=category, owner=user)
    mat.save()

    return {"status": "success", "data": {"id": str(mat.id)}}


def material_by_id():
    id = request.form.get("id", default=None)
    if not id:
        return {"status": "failed", "data": "id required"}
    material = Material.objects(id=id).first()
    if not material:
        return {"status": "failed", "data": "id does not exist"}
    return {"status": "success", "data": {
        "title": material.title,
        "category": material.category,
        "content": material.content,
        "owner_name": material.owner.username
    }}


def material_search():
    text = request.form.get("text", default=None)
    if not text:
        return {"status": "failed", "data": "text required"}

    materials = Material.objects.search_text(text)
    return {"status": "success", "data":
        [{"id": str(material.id),
          "title": material.title,
          "category": material.category,
          # "content": material.content,
          "owner_name": material.owner.username} for material in materials]
    }


def material_delete():
    #  验证登陆
    token = request.form.get("token")
    if not token:
        return {"status": "failed", "data": "token required"}
    user = auth_by_token(token)
    if not user:
        return {"status": "failed", "data": "invalid token"}

    id = request.form.get("id", default=None)
    if not id:
        return {"status": "failed", "data": "id required"}
    material = Material.objects(id=id).first()
    if not material:
        return {"status": "failed", "data": "id does not exist"}

    if material.owner != user:
        return {"status": "failed", "data": "forbidden"}

    material.delete()
    return {"status": "success"}
#  import os
# from flask import Flask,request,Blueprint
# from flask_mongoengine import MongoEngine
# from mongoengine import  Document, StringField, ReferenceField, DateTimeField,EmbeddedDocumentField,ListField,EmbeddedDocument
# from flaskr.auth import auth_by_token

# bp = Blueprint('material', __name__, url_prefix='/material')

# class Material(Document):
#     title = StringField(required=True)
#     content = StringField(required=True)
#     owner = ReferenceField('User',required=True)
#     category = StringField(required=True)#资料类型？
#     #搜索时所占权重?
#     meta = {'indexes':[{
#         'fields':['$title','content'],
#         'default_language':'English',#默认语言是英语
#         'weights':{'title':10,'content':2}
#     }]}

# #未登录也可进入，因而要改
# @bp.route('/material_add',methods=['POST'])
# def material_add():
#     # 验证登陆
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}

#     if 'title' in request.form:
#         title = request.form["title"]
#     else:
#         return {"status":"failed",'data':"title required"}
#     if 'content' in request.form:
#         content=request.form['content']
#     else:
#         return {"status":"failed",'data':"content required"}
#     if 'category' in request.form:
#         category = request.form['category']
#     else:
#         return {"status":"failed",'data':"category required"}
#     if user.type_ not in ['teacher','student']:
#         return {"status":"failed",'data':"invalid user type"}
#     if user.type_ == 'teacher' and category not in ['经典教案','网课视频','学生笔记','教材链接']:
#         return {'status':"failed","data":"category invalid"}
#     if user.type_ == 'student' and category not in ['学生笔记','网课视频','教材链接']:#教案学生和教师还分吗？
#       return {'status':'failed','data':'category invalid'}

#     mat = Material(title=title,content=content,category=category,owner=user)
#     mat.save()

#     return {'status':"success","data":{'id':str(mat.id)}}

# @bp.route('/material_by_id',methods=['POST'])
# def meterial_by_id():
#     id = request.form.get('id',default=None)
#     if not id:
#         return {'status':'failed','data':'id required'}
#     material = Material.objects(id=id).first()
#     if not material:
#         return {'status':'failed','data':'id does not exist'}
#     return {'status':'success','data':{
#         'title':material.title,
#         'category':material.category,
#         'content':material.content,
#         'owner_name':material.owner.username
#     }}

# @bp.route('/material_search',methods=['POST'])
# def material_search():
#     text = request.form.get('text',default=None)
#     if not text:
#         return {'status':'failed',"data":'text required'}

#     materials = Material.objects.search_text(text)
#     return {'status':"success",'data':
#             [{'id':str(material.id),
#               'title':material.title,
#               'category':material.category,
#               'content':material.content,
#               'owner_name':material.owner.username} for material in materials#for循环
#             ]
#     }

# @bp.route('/material_delete',methods=['POST'])
# def material_delete():
#     # 验证登陆
#     token = request.form.get('token')
#     if not token:
#         return {'status':"failed",'data':'token requied'}
#     user = auth_by_token(token)
#     if not user:
#         return {'status':'failed','data':'invalid token'}

#     id = request.form.get('id',default=None)
#     if not id:
#         return {"status":'failed','data':'id required'}
#     material = Material.objects(id=id).first()
#     if not material:
#         return {'status':'failed','data':'id does not exist'}

#     if material.owner != user:
#         return {'status':'failed','data':'forbidden'}

#     material.delete()
#     return {'status':'success'}