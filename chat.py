# import os
# from flask import Flask,request
# from flask_mongoengine import MongoEngine
# from mongoengine import  Document, StringField, ReferenceField, DateTimeField,EmbeddedDocumentField,ListField,EmbeddedDocument
# from flask_socketio import SocketIO,join_room,send,emit
# from .. import socketio,auth_by_token
# #聊天
# @socketio.on('message')
# def on_message(data):
#     token = data.get('token')
#     if not token:
#         return {'status':'failed','data':'token required'}
#     to = data.get('to')
#     if not to:
#         return {'status':'failed','data':'to required'}
#     message = data.get('message')
#     if not message:
#         return {'status':'failed','data':'message required'}
#     user = auth_by_token(token)
#     if not user:
#         return {'status':'failed','data':'token invalid'}
#     send(message, room="{}{}".format(to,user.username)) #这一句
#     return {'status':'success','data':'message sent'}

# @socketio.on('join')
# def on_join(data):
#     token = data.get('token')
#     if not token:
#         return {'status':'failed','data':'token required'}
#     to = data.get('to')
#     if not to:
#         return {'status':'failed','data':'to required'}
#     user = auth_by_token(token)
#     if not user:
#         return {'status':'failed','data':'token invalid'}
#     #user.username to to
#     join_room(room="{}{}".format(to,user.username))
#     return {'status':'success','data':'you have joined'}
