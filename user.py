import datetime

from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField
from utils import require_arguments,success
from flask import request
import uuid
#错题是否要作为用户的一个属性
#session要不要重新考虑一下

class User(Document):
    username = StringField(required=True)
    password = StringField(required=True)
    type_ = StringField(required=True,regex='(teacher|student)')
    real_name = StringField()
    avatar = StringField()#图片存放位置
    class_name = StringField()
    phone_number = StringField()
    school_name = StringField()
    student_id = StringField()
    email_address = StringField()
    grade_name = StringField()
    qq_number = StringField()


class Token(Document):
    user = ReferenceField('User',required=True)
    token = StringField(required=True)
    expire = DateTimeField(required=True)

def auth_by_password(username,password):
    users = User.objects(username=username)
    if users.count() == 0:
        return False
    if users[0].password != password:
        return False
    return users[0]

def auth_by_token(token,*,min_privilege='student'):
    token = Token.objects(token=token).first()
    if not token:
        raise InvalidArgument('token required')
    if datetime.datetime.now() > token.expire:
        raise InvalidArgument('token required')
    if min_privilege =='admin' and token.user.type_ not in ['teacher']:
        raise InvalidArgument('insufficient permission')
    return token.user

def user_register():
    '''
    route:/user_register
    method:POST
    fields:username,password,type
    usernam不能与已知用户重复
    password不能有空格，长度介于8到16之间
    type只可为teacher，student，admin之一
    '''
    [username,password,type_]=require_arguments('username','password','type')
    if ' ' in username:
        raise InvalidArgument('invalid username')
    if type_ not in ['student','teacher']:
        raise InvalidArgument('user type invalid')
    if User.objects(username=username).count()>0:
        raise InvalidArgument('duplicated username')
    if len(password)>16 or len(password)<8:
        raise InvalidArgument('password length should be between 8 and 16')
    if ' ' in password:
        raise InvalidArgument('Invalid password')
    User(username=username,password=password,type_=type_).save()
    return {'status':'success'}

def fill_information():
    [token,real_name,student_id,email_address,phone_number,school_name,grade_name,class_name]=require_arguments('token','real_name','student_id','email_address','phone_number','school_name','grade_name','class_name')
    user = auth_by_token(token)
    if 'qq_number' in request.form:
        qq_number = request.form['qq_number']
        if qq_number != None:
            if ' ' in qq_number:
                raise InvalidArgument('invalid qq number')
            if len(qq_number)<5 or len(qq_number)>10:
                raise InvalidArgument('invalid qq number')
            user.qq_number=qq_number
    if len(phone_number)!=11:
        raise InvalidArgument('invalid phone number')
    if '@' not in email_address:
        raise InvalidArgument('invalid email address')

    if User.objects(email_address=email_address).count()>0:
        if email_address == user.email_address:
            pass 
        else:
            raise InvalidArgument('duplicated email address')

    user.real_name = real_name
    user.phone_number=phone_number
    user.email_address=email_address
    user.student_id=student_id
    user.school_name=school_name
    user.grade_name=grade_name
    user.class_name = class_name
    user.save()
    return {'status':'success'}

# def get_info():
#     [token] = require_arguments('token')
#     user = auth_by_token(token)
#     real_name = user.real_name
#     student_id = user.student_id
#     email_address = user.email_address
#     phone_number = user.phone_number
#     qq_number = user.qq_number
#     school_name = user.school_name
#     grade_name = user.grade_name
#     class_name = user.class_name
#     return success({
#     'real_name':real_name,
#     'student_id':student_id,
#     'email_address':email_address,
#     'phone_number':phone_number,
#     'qq_number':qq_number,
#     'school_name':school_name,
#     'grade_name':grade_name,
#     'class_name':class_name})

def user_login():
    [username,password]=require_arguments('username','password')
    user = auth_by_password(username,password)
    if not user:
        raise InvalidArgument('invalid username or password')
    id = str(uuid.uuid4()).replace('-','')
    token = Token(user=user,token=id,expire=datetime.datetime.now()+datetime.timedelta(days=30))
    token.save()
    return success({'token':id,'type':user.type_})

#改密码要改token吗？
def change_password():
    [token,email_address,phone_number,old_password,new_password]=require_arguments('token','email_address','phone_number','old_password','new_password')
    user = auth_by_token(token)
    
     # 前端来做
    # if 'confirm_password' in request.form:
    #     confirm_password = request.form['confirm_password']
    # else:
    #     return {'status':'failed','data':'confirm password required'}
    # if new_password != confirm_password:
    #     return {'status':'failed','data':'the confirm password differs from the former one'}use
    if email_address != user.email_address:
        raise InvalidArgument('email_address is wrong')
    if phone_number != user.phone_number:
        raise InvalidArgument('phone number is wrong')
    if old_password == new_password:
        raise InvalidArgument('the new password is the same as the old')
    if len(new_password)<8 or len(new_password)>16:
        raise InvalidArgument('the length of password should be between 8 and 16')
    if ' ' in new_password:
        raise InvalidArgument('illegal character in password')
    if old_password != user.password:
        raise InvalidArgument('invalid password')
    user.password=new_password
    user.save()
    return success(user.password)#这个要改，不能直接传密码
#修改其余个人资料,是点一个属性的修改按钮修改一个请求吗？

def change_username():
    [token,new_username]=require_arguments('token','username')
    user = auth_by_token(token)
    if ' ' in new_username:
        raise InvalidArgument('invalid username')
    if new_username == user.username:
        raise InvalidArgument("username hasn't been changed")
    if User.objects(username=new_username).count()>0:
        raise InvalidArgument('duplicated username')
    user.username=new_username
    user.save()
    return {'status':'success'}

#学生用户可能没有权限？
def change_class_name():
    [token,new_class_name]=require_arguments('token','new_class_name')
    user = auth_by_token(token)
    if new_class_name == user.class_name:
        raise InvalidArgument("class_name hasn't been changed")
    user.class_name=new_class_name
    user.save()
    return {'status':'success'}


def change_phone_number():
    [token,new_phone_number]=require_arguments('token','new_phone_number')
    user = auth_by_token(token)
    if ' ' in new_phone_number:
        raise InvalidArgument('invalid phonename')
    if new_phone_number == user.phone_number:
        raise InvalidArgument("phone number hasn't been changed")
    if User.objects(phone_number=new_phone_number).count()>0:
        raise InvalidArgument('duplicated phone number')
    user.phone_number=new_phone_number
    user.save()
    return {'status':'success'}


def logout():
    token=require_arguments('token')
    Token.objects(token=token).delete()
    return {'status':'success'}


#def get_time():
    

def user_info():
    [token] = require_arguments("token")
    user = auth_by_token(token)
    if not user:
        raise InvalidArgument("token invalid")
    return success({
        "username": user.username,
        "type": user.type
    })

def user_full_info():
    [token] = require_arguments("token")
    user = auth_by_token(token)
    if not user:
        raise InvalidArgument("token invalid")
    # if user.real_name==None and user.student_id==None:
    #     if user.phone_number == None and user.email_address == None:
    #         if user.qq_number == None and user.school_name == None:
    #             if user.grade_name == None and user.class_name == None:
    #                 return None
    return success({
        'real_name':user.real_name,
        'student_id':user.student_id,
        'phone_number':user.phone_number,
        'email_address':user.email_address,
        'qq_number':user.qq_number,
        'school_name':user.school_name,
        'grade_name':user.grade_name,
        'class_name':user.class_name
    })

def send_password():
    [email_address,phone_number] = require_arguments('email_address','phone_number')
    user = User.objects(email_address=email_address).first()
    if user.phone_number != phone_number:
        raise InvalidArgument('invalid email address or phone number')
    return user.password
