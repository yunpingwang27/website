# import os
# from flask import request,Blueprint
# from flask_mongoengine import MongoEngine
# from mongoengine import  Document, StringField, ReferenceField, DateTimeField,EmbeddedDocumentField,ListField,EmbeddedDocument
# from flaskr.auth import auth_by_token

# bp = Blueprint('paper', __name__, url_prefix='/paper')

# class Paper_unit(EmbeddedDocument):
#     question = StringField(required=True)
#     answer = StringField(required=True)
#     analyze = StringField()

# class Paper(Document):
#     content = ListField(EmbeddedDocumentField(Paper_unit))
#     title = StringField(required=True)
#     about = StringField(required=True)

# # @bp.route('/do_paper',methods=True)
# # def do_paper():
    

 