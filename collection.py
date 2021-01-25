import os
from flask import request,Blueprint
from flask_mongoengine import MongoEngine
from mongoengine import  Document, StringField, ReferenceField, DateTimeField,EmbeddedDocumentField,ListField,EmbeddedDocument
from material import Material
from auth import auth_by_token

bp = Blueprint('collection', __name__, url_prefix='/collection')

class Collection_unit(EmbeddedDocument):
    content = ReferenceField('Material',required=True)
    annotation = StringField()
    collection = ReferenceField('Collection',requied=True)
#收藏夹
class Collection(Document):
    collect = ListField(EmbeddedDocumentField(Collection_unit))
    title = StringField(required=True)
    owner = ReferenceField('User',required=True)
    meta = {'indexes':[{
        'fields':['$title'],
        'default_language':'English',#默认语言是英语
    }]}

@bp.route('/collection_build',methods=['POST'])
def collection_build():
    #验证登陆
    token = request.form.get('token')
    if not token:
        return {"status":"failed","data":"token required"}
    user = auth_by_token(token)
    if not user:
        return {"status":"failed",'data':"invalid token"}
    if 'title' in request.form:
        title = request.form['title']
    else:
        return {'status':'failed','data':'title required'}
    if Collection.objects(title=title).count()>0:
        return {'status':'failed',"data":"duplicated collection name"}
    collection = Collection(title=title,owner=user)
    collection.save()
    return {'status':'success','data':str(collection.id)}

@bp.route('/collection_by_id',methods=['POST'])
def collection_by_id():
    id = request.form.get('id',default=None)
    if not id:
        return {'status':'failed','data':'id required'}
    collection = Collection.objects(id=id).first()
    if not collection:
        return {'status':'failed','data':'id does not exist'}
    return {'status':'success','data':{
        'title':collection.title,
        'content':collection.collect,
        'owner_name':collection.owner.username
    }}


@bp.route('/collect_add',methods=['POST'])
def collection_add():
    #验证登陆
    token = request.form.get('token')
    if not token:
        return {"status":"failed","data":'token required'}
    user = auth_by_token(token)
    if not user:
        return {"status":"failed",'data':"invalid token"}
    id = request.form.get('id',default=None)
    if not id:
        return {'status':'failed','data':'id required'}
    material = Material.objects(id=id).first()
    if not material:
        return {'status':'failed','data':'id does not exist'}
    if 'collection_name' in request.form:
        collection_name=request.form['collection_name']
    else:
        return {'status':'failed','data':'collection name required'}
    if 'annotation' in request.form:
        annotation = request.form['annotation']
    else:
        return {'status':'failed','data':'annotation required'}
    collection = Collection.objects(title=collection_name).first()
    collection.collect.append(Collection_unit(annotation=annotation,content=material,collection=collection))
    #Collection_unit(annotation=annotation,content=material,collection=collection).save()#这里出错
    
    return {'status':'success','data':{
        'title': collection.title,
        'owner':collection.owner,
        'material':collection.collect,
        'content':material.title
    }}


@bp.route('/collection_search',methods=['POST'])
def collection_search():
        text = request.form.get('text',default=True)
        if not text:
            return {'status':'failed',"data":'text required'}
        collections = Collection.objects.search_text(text)
        #problems = Problem.objects.search_text(text)
        #要是找不到怎么判断与处理
        return {'status':"success",'data':{
            'collection':collections
        }}
        

@bp.route('/collection_delete',methods=['POST'])
def collection_delete():
    # 验证登陆
    token = request.form.get('token')
    if not token:
        return {'status':"failed",'data':'token requied'}
    user = auth_by_token(token)
    if not user:
        return {'status':'failed','data':'invalid token'}

    id = request.form.get('id',default=None)
    if not id:
        return {"status":'failed','data':'id required'}
    collection = Collection.objects(id=id).first()
    if not collection:
        return {'status':'failed','data':'id does not exist'}

    if collection.owner != user:
        return {'status':'failed','data':'forbidden'}

    collection.delete()
    return {'status':'success'}
    