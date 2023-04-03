from flask import request
from datetime import datetime
from application.models.auth import ActiveSession
from application.database import db
from json import loads as json_loads
from functools import wraps

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
        activeSession = db.session.query(ActiveSession).filter(ActiveSession.ver_code == token, user_id=key).first()
        
        if activeSession != None:
            activeSession.last_access_datetime = datetime.now()
            db.session.add(activeSession)
            db.session.commit()
            res = {"success":True, "message": "Success"}
        else:
            res = {"success":False, "message": "Session expired, Login again to continue.", "custom_code":7}
            
    except Exception as e:
        res = {"success":False, "message": e}
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
                result = validate(token=token, key=data.get('key', ""))
                if result['success'] == True:
                    return fn(*args, **Kwargs)
                else:
                    return ResponseObj(False,result['message'], 401, custom_code=100)
            except Exception as e:
                return ResponseObj(False,"Internal Server Error", 500, exceptionObj=e, custom_code=101)
                
        return wrapper

    return wrapper_main