# import functools
# import datetime
# import uuid
# import os
# from flask import Blueprint, request
# from mongoengine import  Document, StringField, ReferenceField, DateTimeField,EmbeddedDocumentField,ListField,EmbeddedDocument
# from werkzeug.utils import secure_filename
# from flask import Flask,request
# from flask_mongoengine import MongoEngine
# #from werkzeug.security import check_password_hash, generate_password_hash

# bp = Blueprint('auth', __name__, url_prefix='/auth')

# class User(Document):
#     username = StringField(required=True)
#     password = StringField(required=True)
#     classname = StringField(required=True)
#     phonenum = StringField(required=True)
#     type_ = StringField(required=True)

# class Token(Document):
#     user = ReferenceField('User',required=True)
#     token = StringField(required=True)
#     expire = DateTimeField(required=True)

# # @bp.route('/')
# # def hello_world():
# #     return 'Hello!'

# @bp.route('/user_register',methods=['POST'])
# def user_register():
#     if 'username' in request.form:
#         username = request.form['username']
#     else:
#         return {'status':'failed','data':'username required'}
#     if 'password' in request.form:
#         password = request.form['password']
#     else:
#         return {'status':'failed','data':'password required'}
#     # if 'confirm_password' in request.form:
#     #     confirm_password = request.form['confirm_password']
#     # else:
#     #     return {'status':'failed','data':'confirm password required'}
#     if 'type_' in request.form:
#         type_ = request.form['type_']
#     else:
#         return {'status':'failed','data':'type required'}
#     if 'classname' in request.form:
#         classname = request.form['classname']
#     if 'phonenum' in request.form:
#         phonenum = request.form['phonenum']
#     if len(phonenum)!=11 or ' ' in phonenum:
#         return {'status':'failed','data':'invalid phonenum'}
#     if ' ' in username:
#         return {'status':'failed','data':'invalid username'}
#     if type_ not in ['student','teacher']:
#         return {'status':'failed','data':'invalid type'}
#     # if password != confirm_password:
#     #     return {'status':'failed','data':'the confirm password differs from the former one'}
#     if len(password)<8 or len(password)>16:
#         return {'status':'failed','data':'the length of password should be between 8 and 16'}
#     if ' ' in password:
#         return {'status':'failed',"data":'illegal character in password'}
#     if User.objects(username=username).count()>0:
#         return {'status':'failed',"data":"duplicated username"}
#     User(username=username,password=password,type_=type_,classname=classname,phonenum=phonenum).save()
#     return {'status':"success"}

# def auth(username,password):
#     users = User.objects(username=username)
#     if users.count()==0:
#         return False
#     if users[0].password != password: #?为何要【0】
#         return False
#     return users[0]

# def auth_by_token(token):
#     token=Token.objects(token=token).first()
#     if not token:
#         return False
#     if datetime.datetime.now()>token.expire:
#         return False
#     return token.user

# #是不是要改成by token？
# @bp.route('/user_login',methods=['POST'])
# def user_login():
#     if 'username' in request.form:
#         username = request.form['username']
#     else:
#         return {'status':'failed','data':'username required'}
#     if 'password' in request.form:
#         password = request.form['password']
#     else:
#         return {'status':'failed','data':"password required"}
#     user = auth(username,password)
#     if not user:
#         return {"status":"failed","data":'invalid username or password'}
#     #id = str(uuid.uuid4()).replace('-','')
#     id = str(uuid.uuid4())
#     token = Token(user=user,token=id,expire=datetime.datetime.now()+datetime.timedelta(days=30))
#     token.save()
#     return {"status":"success","data":{
#         "token":id
#     }}

# #改密码要改token吗？
# @bp.route('/change_password',methods=['POST'])
# def change_password():
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     if 'old_password' in request.form:
#         old_password = request.form['old_password']
#     else:
#         return {'status':'failed','data':'old password required'}
#     if 'new_password' in request.form:
#         new_password = request.form['new_password']
#     else:
#         return {'status':'failed','data':'new password required'}
#     # 前端来做
#     # if 'confirm_password' in request.form:
#     #     confirm_password = request.form['confirm_password']
#     # else:
#     #     return {'status':'failed','data':'confirm password required'}
#     # if new_password != confirm_password:
#     #     return {'status':'failed','data':'the confirm password differs from the former one'}
#     if old_password == new_password:
#         return {'status':'failed','data':'the new password is the same as the old'}
#     if len(new_password)<8 or len(new_password)>16:
#         return {'status':'failed','data':'the length of password should be between 8 and 16'}
#     if ' ' in new_password:
#         return {'status':'failed',"data":'illegal character in password'}
#     user.password=new_password
#     user.save()
#     return {'status':'success','data':user.password}

# #修改其余个人资料,是点一个属性的修改按钮修改一个请求吗？
# @bp.route('/change_username',methods=['POST'])
# def change_username():
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     if 'new_username' in request.form:
#         new_username = request.form['new_username']
#         user.username=new_username
#         user.save()
#         return {'status':'success'}
#     else:
#         return {'status':'failed','data':'new_username required'}

# @bp.route('/change_classname',methods=['POST'])
# def change_classname():
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     if 'new_classname' in request.form:
#         new_classname = request.form['new_classname']
#         user.classname=new_classname
#         user.save()
#         return {'status':'success'}
#     else:
#         return {'status':'failed','data':'new_classname required'}

# @bp.route('/change_phonenum',methods=['POST'])
# def change_phonenum():
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     if 'new_phonenum' in request.form:
#         new_phonenum = request.form['new_phonenum']
#         user.phonenum=new_phonenum
#         user.save()
#         return {'status':'success'}
#     else:
#         return {'status':'failed','data':'new_phonenum required'}

# @bp.route('/user_logout',methods=['POST'])
# def user_logout():
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     Token.objects(token=token).delete()
#     return {'status':'success'}
