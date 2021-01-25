import datetime
import os

from flask import Flask, request,send_file
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO, join_room, send, emit
from mongoengine import Document, StringField, ReferenceField, DateTimeField
from werkzeug.utils import secure_filename
import uuid
import problem
import user 
import other_note
import event
import process
import material
from user import auth_by_token
from exception import InvalidArgument


app = Flask(__name__, static_url_path='', static_folder='static')
# This would usually come from your config file
DB_URI = "mongodb+srv://yunping:ping020627@cluster0.nfple.mongodb.net/phystudy?retryWrites=true&w=majority"
#"mongodb+srv://yunping:ping020627@phystudy.mongodb.net/phystudy?retryWrites=true&w=majority"

app.config["MONGODB_HOST"] = DB_URI
app.config['MONGODB_SETTINGS'] = {
    'db': 'phystudy'}

socketio = SocketIO(app)

db = MongoEngine(app)


#client = pymongo.MongoClient("mongodb://yunping:<password>@cluster0-shard-00-00.nfple.mongodb.net:27017,cluster0-shard-00-01.nfple.mongodb.net:27017,cluster0-shard-00-02.nfple.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-72plf8-shard-0&authSource=admin&retryWrites=true&w=majority")
#db = client.test


class Material(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    owner = ReferenceField('User', required=True)
    category = StringField(required=True)

    meta = {'indexes': [
        {'fields': ['$title', "$content"],
         'default_language': 'english',
         'weights': {'title': 10, 'content': 2}
         }
    ]}


@app.errorhandler(InvalidArgument)
def handle_invalid_usage(error):
    return {"status": "failed", "data": error.message}


@app.errorhandler(Exception)
def handle_exception(error):
    return {"status": "fatal", "data": str(error)}


class Problem(Document):
    problem = StringField(required=True)
    answer = StringField()
    test = StringField()





UPLOAD_FOLDER = '/home/phystudy'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return {"status": "failed", "data": "file required"}
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {"status": "failed", "data": "file required"}

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save('/home/phystudy' + filename)
        return {"status": "success", "data": {"path": "/uploaded_files/" + filename}}

@app.route('/download_file', methods=['POST'])
def download_file():
    # check if the post request has the file part
    file_name = request.form.get('file_name')
    # if user does not select file, browser also
    # submit an empty part without filename
    return send_file('/home/phystudy'+file_name)



@socketio.on('message')
def on_message(data):
    token = data.get("token")
    if not token:
        return {"status": "failed", "data": "token required"}
    to = data.get("to")
    if not to:
        return {"status": "failed", "data": "to required"}
    message = data.get('message')
    if not message:
        return {"status": "failed", "data": "message required"}
    user = auth_by_token(token)
    if not user:
        return {"status": "failed", "data": "token invalid"}
    send(message, room='{}{}'.format(to,user.username))
    return {"status": "success", "data": "message sent"}


@socketio.on('join')
def on_join(data):
    token = data.get("token")
    if not token:
        return {"status": "failed", "data": "token required"}
    to = data.get("to")
    if not to:
        return {"status": "failed", "data": "to required"}
    user = auth_by_token(token)
    if not user:
        return {"status": "failed", "data": "token invalid"}
    # user.username to to
    join_room('{}{}'.format(user.username,to))
    return {"status": "success", "data": "you have joined"}


app.add_url_rule('/user_register', view_func=user.user_register, methods=['POST'])
app.add_url_rule('/user_login', view_func=user.user_login, methods=['POST'])
app.add_url_rule('/change_info',view_func=user.fill_information,methods=['POST'])
app.add_url_rule('/user_info', view_func=user.user_info, methods=['POST'])
app.add_url_rule('/user_full_info',view_func=user.user_full_info,methods=['POST'])
app.add_url_rule('/user_fill_info',view_func=user.fill_information,methods=['POST'])
app.add_url_rule('/forgot_password',view_func=user.send_password,methods=['POST'])
app.add_url_rule('/reset_password',view_func=user.change_password,methods=['POST'])

app.add_url_rule('/event_add',view_func=event.add_event,methods=['POST'])
app.add_url_rule('/event_edit',view_func=event.edit_event,methods=['POST'])
app.add_url_rule('/user_event',view_func=event.get_user_event,methods=['POST'])

app.add_url_rule('/problem/add', view_func=problem.problem_add, methods=['POST'])
app.add_url_rule('/new_assignment', view_func=problem.new_assignment, methods=['POST'])
app.add_url_rule('/problems_get', view_func=problem.problems_get, methods=['POST'])

app.add_url_rule('/other_note/add',view_func=other_note.note_add,methods=['POST'])
app.add_url_rule('/other_note/edit',view_func=other_note.note_edit,methods=['POST'])
app.add_url_rule('/user_other_note',view_func=other_note.user_note,)

app.add_url_rule('/process_add',view_func=process.add_process,methods=['POST'])
app.add_url_rule('/user_process',view_func=process.user_process,methods=['POST'])
app.add_url_rule('/process_edit',view_func=process.edit_process,methods=['POST'])
app.add_url_rule('/process_delete',view_func=process.delete_process,methods=['POST'])

app.add_url_rule('/material_add',view_func=material.material_add,methods=['POST'])
app.add_url_rule('/material_delete',view_func=material.material_delete,methods=['POST'])

if __name__ == '__main__':
    socketio.run(app)

# import datetime
# import uuid
# import os
# from werkzeug.utils import secure_filename
# from flask import Flask,request,Blueprint
# from flask_mongoengine import MongoEngine
# from mongoengine import  Document, StringField, ReferenceField, DateTimeField,EmbeddedDocumentField,ListField,EmbeddedDocument
# from flask_socketio import SocketIO,join_room,send,emit
#密码的加密存储hash
#选项select field，material更改
#系统消息，用户消息修改
#点赞
#微信登录
#分解app功能模块
#全网搜索，搜索无结果处理



# app = Flask(__name__,static_url_path='',static_folder='static')
# app.config['MONGODB_SETTINGS']={'db':'phystudy'}
# socketio = SocketIO(app)

# db = MongoEngine(app)

# class User(Document):
#     username = StringField(required=True)
#     password = StringField(required=True)
#     classname = StringField(required=True)
#     phonenum = StringField(required=True)
#     type_ = StringField(required=True)

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

# class Token(Document):
#     user = ReferenceField('User',required=True)
#     token = StringField(required=True)
#     expire = DateTimeField(required=True)

# @app.route('/')
# def hello_world():
#     return 'Hello!'

# @app.route('/user_register',methods=['POST'])
# def user_register():
#     if 'username' in request.form:
#         username = request.form['username']
#     else:
#         return {'status':'failed','data':'username required'}
#     if 'password' in request.form:
#         password = request.form['password']
#     else:
#         return {'status':'failed','data':'password required'}
#     if 'confirm_password' in request.form:
#         confirm_password = request.form['confirm_password']
#     else:
#         return {'status':'failed','data':'confirm password required'}
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
#     if password != confirm_password:
#         return {'status':'failed','data':'the confirm password differs from the former one'}
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
# @app.route('/user_login',methods=['POST'])
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
# @app.route('/change_password',methods=['POST'])
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
# @app.route('/change_username',methods=['POST'])
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

# @app.route('/change_classname',methods=['POST'])
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

# @app.route('/change_phonenum',methods=['POST'])
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

# @app.route('/user_logout',methods=['POST'])
# def user_logout():
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     Token.objects(token=token).delete()
#     return {'status':'success'}


# #未登录也可进入，因而要改
# @app.route('/material_add',methods=['POST'])
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

# @app.route('/material_by_id',methods=['POST'])
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

# @app.route('/material_search',methods=['POST'])
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

# @app.route('/material_delete',methods=['POST'])
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

# class Problem(Document):
#     problem = StringField(required=True)
#     answer = StringField(required=True)
#     test = StringField(required=True)#?

# @app.route('/test_query')
# def test_query():
#     return {"data":Problem.objects.as_pymongo()}#as_pymongo

# @app.route('/test_clear')
# def test_clear():
#     #这个函数有什么用处？将problem中的所有题目均删除？
#     for p in Problem.objects:
#         p.delete()
#     return 'success'

# #from the web
# class Note_unit_1(EmbeddedDocument):
#     annotation = StringField(required=True)
#     main_content = ReferenceField('Problem',required=True)

# class Collection_unit(EmbeddedDocument):
#     content = ReferenceField('Material',required=True)
#     annotation = StringField()
#     collection = ReferenceField('Collection',requied=True)
# #收藏夹
# class Collection(Document):
#     collect = ListField(EmbeddedDocumentField(Collection_unit))
#     title = StringField(required=True)
#     owner = ReferenceField('User',required=True)
#     meta = {'indexes':[{
#         'fields':['$title'],
#         'default_language':'English',#默认语言是英语
#     }]}

# @app.route('/collection_build',methods=['POST'])
# def collection_build():
#     #验证登陆
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     if 'title' in request.form:
#         title = request.form['title']
#     else:
#         return {'status':'failed','data':'title required'}
#     if Collection.objects(title=title).count()>0:
#         return {'status':'failed',"data":"duplicated collection name"}
#     collection = Collection(title=title,owner=user)
#     collection.save()
#     return {'status':'success','data':str(collection.id)}

# @app.route('/collection_by_id',methods=['POST'])
# def collection_by_id():
#     id = request.form.get('id',default=None)
#     if not id:
#         return {'status':'failed','data':'id required'}
#     collection = Collection.objects(id=id).first()
#     if not collection:
#         return {'status':'failed','data':'id does not exist'}
#     return {'status':'success','data':{
#         'title':collection.title,
#         'content':collection.collect,
#         'owner_name':collection.owner.username
#     }}


# @app.route('/collect_add',methods=['POST'])
# def collection_add():
#     #验证登陆
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":'token required'}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     id = request.form.get('id',default=None)
#     if not id:
#         return {'status':'failed','data':'id required'}
#     material = Material.objects(id=id).first()
#     if not material:
#         return {'status':'failed','data':'id does not exist'}
#     if 'collection_name' in request.form:
#         collection_name=request.form['collection_name']
#     else:
#         return {'status':'failed','data':'collection name required'}
#     if 'annotation' in request.form:
#         annotation = request.form['annotation']
#     else:
#         return {'status':'failed','data':'annotation required'}
#     collection = Collection.objects(title=collection_name).first()
#     collection.collect.append(Collection_unit(annotation=annotation,content=material,collection=collection))
#     #Collection_unit(annotation=annotation,content=material,collection=collection).save()#这里出错
    
#     return {'status':'success','data':{
#         'title': collection.title,
#         'owner':collection.owner,
#         'material':collection.collect,
#         'content':material.title
#     }}


# @app.route('/collection_search',methods=['POST'])
# def collection_search():
#         text = request.form.get('text',default=True)
#         if not text:
#             return {'status':'failed',"data":'text required'}
#         collections = Collection.objects.search_text(text)
#         #problems = Problem.objects.search_text(text)
#         #要是找不到怎么判断与处理
#         return {'status':"success",'data':{
#             'collection':collections
#         }}
        

# @app.route('/collection_delete',methods=['POST'])
# def collection_delete():
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
#     collection = Collection.objects(id=id).first()
#     if not collection:
#         return {'status':'failed','data':'id does not exist'}

#     if collection.owner != user:
#         return {'status':'failed','data':'forbidden'}

#     collection.delete()
#     return {'status':'success'}
    

# class Paper_unit(EmbeddedDocument):
#     question = StringField(required=True)
#     answer = StringField(required=True)
#     analyze = StringField()

#class Answer()

# class Paper(Document):
#     content = ListField(EmbeddedDocumentField(Paper_unit))
#     title = StringField(required=True)
#     about = StringField(required=True)

# @app.route('/do_paper',methods=['POST'])
# def do_paper():
#     if 

    

# class Note_from_web(Document):
#     """
#     原内容(包括个人上传的照片等，题目，别的暂时不支持)
#     批注（用户输入的内容）
#     类型：学生个人笔记
#     收藏
#     错题集
#     """ 
#     note_title = StringField(required=True)
#     note_type = StringField(required=True)
#     note_owner = ReferenceField('User',required = True)#一个对象对应一个用户
#     main_body=ListField(EmbeddedDocumentField('Note_unit_1'))


# @app.route('/note_build',methods=['POST'])
# def note_build():
#     #验证登陆
#     token = request.form.get('token')
#     if not token:
#         return {"status":"failed","data":"token required"}
#     user = auth_by_token(token)
#     if not user:
#         return {"status":"failed",'data':"invalid token"}
#     if 'note_title' in request.form:
#         note_title = request.form['note_title']
#     else:
#         return {'status':'failed','data':'notebook title required'}
#     if 'note_type' in request.form:
#         note_type = request.form['note_type']
#     else:
#         return {'status':'failed','data':'notebook type required'}
#     if note_type not in ['收藏','错题']:
#         return {'status':'failed','data':'notebook type invalid'}
#     note = Note_from_web(note_title=note_title,note_type=note_type,note_owner=user)#?
#     #main_body怎么设置
#     note.save()
#     return {'status':"success","data":{'id':str(note.id)}}

# @app.route('/note_by_id',methods=['POST'])
# def note_by_id():
#     id = request.form.get('id',default=None)
#     if not id:
#         return {'status':'failed','data':'id required'}
#     note = Note_from_web.objects(id=id).first()
#     if not note:
#         return {'status':'failed','data':'id does not exist'}
#     return {'status':'success','data':{
#         'title':note.title,
#         'category':note.category,
#         'content':note.content,
#         'owner_name':note.owner.username
#     }}

# @app.route('/note_add',methods=['POST'])
# def note_add():
#     #验证登陆
#     id = request.form.get('id',default=None)
#     if not id:
#         return {'status':'failed','data':'id required'}







# UPLOAD_FOLDER = '/path/to/the/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS #上一行末的反斜线是啥意思，换行吗？

# @app.route('/upload_file', methods=['POST'])
# def upload_file():
#     # check if the post request has the file part
#     if 'file' not in request.files:
#         return {'status':'failed','data':'no file part'}
#     file = request.files['file']#不再是request.forms了
#     # if user does not select file, browser also
#     # submit an empty part without filename
#     if file.filename == '':
#         return {'status':'failed','data':'No selected files'}
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return {'status':'success'}


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

    



# if __name__=='main':
#     app.run()