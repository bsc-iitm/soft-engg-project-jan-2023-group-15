from flask import request
from datetime import datetime
from application.models.auth import ActiveSession
from application.models.user import User
from application.database import db
from json import loads as json_loads
from functools import wraps
from flask_restful import Resource

def ResponseObj(success=True, message="", code=200, data={}, exceptionObj = {}, custom_code=200):
    to_return = {"success": success, "message": message, "data": data, "code": custom_code}
    print("Exception Raised:: ", exceptionObj)
    print("Return Object:: ", to_return)
    return to_return, code

def validate(token="", key=""):
    if token == "" or key == "":
        return {"success":False, "message": "Auth key and / or token missing" }  
    
    res = {"success":False, "message": "Initalise"}
    try:
        print(token, key)
        activeSession = db.session.query(ActiveSession).filter(ActiveSession.ver_code == token, ActiveSession.user_id==key).first()
        
        if activeSession != None:
            activeSession.last_access_datetime = datetime.now()
            db.session.add(activeSession)
            db.session.commit()
            res = {"success":True, "message": "Success"}
        else:
            res = {"success":False, "message": "Session expired, Login again to continue.", "custom_code":7}
            
    except Exception as e:
        raise Exception(e)
        
    return res

def token_required(method="POST"):
    def wrapper_main(fn):
        @wraps(fn)
        def wrapper(*args, **Kwargs):
            try:
                if "Authorization" not in request.headers:
                    return ResponseObj(False, "Auth Token Missing", 401)
                token = request.headers['Authorization']  # Fetching TOKEN from the header of the API
                print(method)
                if method == "GET":
                    data = request.args
                else:
                    data = json_loads(request.data)
                key = data.get('key', "")
                result = validate(token=token, key=key)
                if result['success'] == True:
                    Kwargs.update({"key":key})
                    return fn(*args, **Kwargs)
                else:
                    return ResponseObj(False,result['message'], 401, custom_code=100)
            except Exception as e:
                return ResponseObj(False,"Internal Server Error", 500, exceptionObj=e, custom_code=101)
                
        return wrapper

    return wrapper_main

class CustomException(Exception):
    pass

class BaseAPIClass(Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.success = True
        self.message = "Success"
        self.code = 200
        self.data = {}
        self.exceptionObj = {}
        self.custom_code = 000
        self.print_log = True

    def _exception_occured(self, e, custom=False):
        self.success = False
        self.message = "Internal Server Error" if not custom else str(e)
        self.code = 400 if custom else 500
        if isinstance(e, CustomException):
            if isinstance(e.args[0], tuple) and len(e.args[0]) > 1:
                self.message = e.args[0][0]
                self.code = e.args[0][1]

        self.exceptionObj = e
        self.data = {}
    
    def _get_response(self):
        return ResponseObj(self.success, self.message, self.code, self.data, self.exceptionObj, self.custom_code)

def get_user(key, admin=False, isActive=True):
    if isActive:
        user = db.session.query(User).filter(User.id == key, User.status == User.ACCOUNT_STATUS.ACTIVE).first()
    else:
        user = db.session.query(User).filter(User.id == key).first()
    if user == None or (admin and user.role != User.Role.ADMIN):
        raise CustomException(("User does not exist", 404))
    return user