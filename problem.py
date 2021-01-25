import datetime
from flask import Flask, request
from flask_mongoengine import MongoEngine
from exception import InvalidArgument
from mongoengine import Document, StringField, ReferenceField, DateTimeField, IntField, ListField, EmbeddedDocument, \
    EmbeddedDocumentListField,EmbeddedDocumentField

from user import auth_by_token, User
from utils import require_arguments, success

#学生写作业一写好多题，怎么拆分呢？
#学生收到作业时是不能附带答案的
#多选少选获一半分
#做题限定时间
#教师布置作业限定students

class Problem(Document):
    problem = StringField(required=True)
    key = StringField(required=True)
    type_ = StringField(required=True,regex='(choice|blank)')
    owner = ReferenceField(User,required=True)
    difficulty = IntField(required=True,min_value=1,max_value=5)

class ScoredProblem(EmbeddedDocument):
    problem = ReferenceField(Problem,required=True)
    point = IntField(required=True)

class Assignment(Document):
    owner = ReferenceField(User,required=True)
    scored_problems = EmbeddedDocumentListField(ScoredProblem,required=True)
    students = ListField(ReferenceField(User))
    #作业布置与时间
    assign_time = DateTimeField(required = True)
    days_given = IntField(required=True,min_value=1)


class AssignmentAnswer(Document):
    assignment = ReferenceField(Assignment,required=True)
    answers = ListField(StringField(),required=True)
    points_get = ListField(IntField())
    #作业上交时间
    submit_time = DateTimeField(required=True)

class FaultAnswer(EmbeddedDocument):
    answer = StringField(required=True)
    scored_problem = EmbeddedDocumentField(ScoredProblem,required=True)

class Fault(Document):
    owner = ReferenceField(User,required=True)
    fault_answer = EmbeddedDocumentField(FaultAnswer,required=True)


def problem_add():

    [token,problem,key,type_,difficulty] = require_arguments('token','problem','key','type_','difficulty')
    user = auth_by_token(token,min_privilege='teacher')
    try:
        difficulty = int(difficulty)
    except ValueError:
        raise InvalidArgument('difficulty must be an integar')
    problem = Problem(problem=problem,key=key,type_=type_,owner=user,difficulty=difficulty).save()

    return success({'id':str(problem.id)})

def problems_get():
    problems = Problem.objects
    print(problems)
    return success([{
        'id':str(problem.id),
        'problem':problem.problem,
        'type':problem.type,
        'difficulty':problem.difficulty
    }for problem in problems])

def assignment_by_id():
    id = require_arguments('id')
    assignment = Assignment.objects(id=id).first()
    if not assignment:
        raise InvalidArgument('id does not exist')    
    # return success({'owner':assignment.owner,
    # 'scored problems':assignment.scored_problems,
    # 'students':assignment.students
    # })
    return success(assignment)

def answer_by_id(id):
    #id = require_arguments('id')
    answer = AssignmentAnswer.objects(id=id).first()
    if not answer:
        raise InvalidArgument('id does not exist')    
    # return success({'owner':assignment.owner,
    # 'scored problems':assignment.scored_problems,
    # 'students':assignment.students
    # })
    return answer

def new_assignment():
    days_given = require_arguments('days_given')
    try:
        days_given = int(days_given)
    except ValueError:
        raise InvalidArgument('days given must be an integar')
    students = request.json.get('student')
    if students is None:
        raise InvalidArgument('students required')
    token = request.json.get('token')
    if not token:
        raise InvalidArgument('token required')
    problems = request.json.get('problems')
    if not problems:
        raise InvalidArgument('problems required')

    user = auth_by_token(token,min_privilege='teacher')
    for student in students:
        if User.objects(id=students).count() == 0:
            raise InvalidArgument('user '+student+' does not exist')
        scored_problems = []
        for problem in problems:
            problem_id = problem.get('id')
            point = problem.get('point')
            scored_problems.append(ScoredProblem(problem=Problem.objects(id=problem_id).first(),point=point))
        date = datetime.datetime.now()
        assignment = Assignment(owner=user,scored_problems=scored_problems,students=students,assign_time=date,days_given=days_given).save()
        return success({'id':str(assignment.id)})        
    
def auto_check_answer():
    [token,answer_id]=require_arguments('token','answer_id')
    user = auth_by_token(token)
    answers = answer_by_id(answer_id)
    assignment = answers.assignment
    problems = answers.assignment.scored_problems

    submit_time = datetime.datetime.now()
    t = assignment.days_given
    deadline = assignment.assign_time + datetime.timedelta(days=t)
    if submit_time > deadline:
        raise InvalidArgument('you have missed the deadline')
    for index,answer in enumerate(answers):
        problem = problems[index]
        if answer == problem.problem.key:
            answer.points_get.append(problems[index].point)
        else:
            fault_answer = FaultAnswer(answer=answer,problems=problem).save()
            fault = Fault(owner=user,fault_answer=fault_answer)
            fault.save()
    answer.save()
    return success(answer)

def fault_report():
    token = require_arguments('token')
    user = auth_by_token(token)
    fault =  Fault(owner=user)
    return fault