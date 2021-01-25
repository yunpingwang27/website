from flask import request
from exception import InvalidArgument

def success(data):
    return {'status':'success','data':data}

def require_arguments(*args):
    ret = []
    for arg in args:
        if arg not in request.form:
            raise InvalidArgument(arg+' required')
        ret.append(request.form[arg])
    return ret

# def may_require_arguments(*args):
#     ret = []
#     for arg in args:
#         if arg not in request.form:
#             ret.append(None)
#         ret.append(request.form[arg])
#     return ret
