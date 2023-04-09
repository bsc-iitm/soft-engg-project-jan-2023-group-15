from flask_restful import reqparse, request
from application.models.user import User
from application.models.auth import ActiveSession
from application.database import db
from application.helpers import BaseAPIClass, CustomException
from jwt import encode
from datetime import datetime
from hashlib import sha256
from application.helpers import token_required

login_req = reqparse.RequestParser()
login_req.add_argument("obj_data", required=True, type=dict, help='OAuth is required')

register_req = reqparse.RequestParser()
register_req.add_argument("username", required=True, type=str, trim=True, help='Username is required')
register_req.add_argument("email", required=True, type=str, trim=True, help='Email is required')

JWT_SECRET_KEY = "wvz^f.wu^ZDtm@X.N{s@9NGXbP[}bWdM"
HASHING_CODE = "Q^v>em/F#jF6HD1nh`2~@O7[TWcVyKA"

def generate_token(user_obj):
    return encode({'user_id': user_obj.id, 'created_at': str(datetime.now())}, key=JWT_SECRET_KEY, algorithm="HS256",)

class Login(BaseAPIClass):
    def _create_active_session(self, user):
        token = generate_token(user)
        print(user.id)
        activeSession = ActiveSession(
            user_id = user.id,
            ver_code = token
        )
        db.session.add(activeSession)
        db.session.commit()
        return activeSession

    def post(self):
        try:
            args = login_req.parse_args()
            obj_data = args.get('obj_data', {})
            
            print(obj_data)
            if len(obj_data) == 0 or not isinstance(obj_data, dict) or "user" not in obj_data or "uid" not in obj_data["user"]:
                raise CustomException("OAuth is invalid")
            
            email = obj_data["user"]["email"]
            password = sha256(obj_data["user"]["uid"].encode("utf-8")).hexdigest()

            user = db.session.query(User).filter(User.email == email).first()

            if user.status==User.ACCOUNT_STATUS.BLOCKED:
                raise CustomException("Your account is blocked")
            
            if user == None:
                username = str(email).split("@")[0]
                profile_picture = obj_data["user"]["photoURL"]
                full_name = obj_data["user"]["displayName"]
                user = User(
                    email = email,
                    password = password,
                    username = username,
                    profile_picture = profile_picture,
                    full_name = full_name
                )
                db.session.add(user)
                db.session.commit()
            else:
                if user.password != password:
                    raise CustomException("Authentication failed")
                
                if user.status==User.ACCOUNT_STATUS.DEACTIVATED:
                    user.status=User.ACCOUNT_STATUS.ACTIVE
                
            activeSession = self._create_active_session(user)
            self.message = "Login successful!"
            self.data = {
                "key":user.id,
                "token":activeSession.ver_code
            }
        except CustomException as e:
            self.custom_code = 1001
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 1002
            self._exception_occured(e, False)
        return self._get_response()

class SupportStaffLogin(Login):

    def post(self):
        try:
            args = login_req.parse_args()
            obj_data = args.get('obj_data', {})
            
            print(obj_data)
            if len(obj_data) == 0 or not isinstance(obj_data, dict) or "user" not in obj_data or "uid" not in obj_data["user"]:
                raise CustomException("OAuth is invalid")
            
            email = obj_data["user"]["email"]
            user = db.session.query(User).filter(User.email == email, User.role==User.Role.SUPPORT_STAFF).first()

            if user.status==User.ACCOUNT_STATUS.BLOCKED:
                raise CustomException("Your account is blocked")
            
            if user == None:
                raise CustomException("You are not registered as support staff, please ask admin to give you access")
            else:
                password = sha256(obj_data["user"]["uid"].encode("utf-8")).hexdigest()
                if user.password == "FIRST_TIME":
                    user.password = password
                    user.profile_picture = obj_data["user"]["photoURL"]
                    user.full_name = obj_data["user"]["displayName"]
                    db.session.add(user)
                    db.session.commit()
                if user.password != password:
                    raise CustomException("Authentication failed")
                if user.status==User.ACCOUNT_STATUS.DEACTIVATED:
                    user.status=User.ACCOUNT_STATUS.ACTIVE
            
            activeSession = self._create_active_session(user)
            self.message = "Login successful!"
            self.data = {
                "key":user.id,
                "token":activeSession.ver_code
            }
        except CustomException as e:
            self.custom_code = 1003
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 1004
            self._exception_occured(e, False)
        return self._get_response()

class SupportStaffRegister(BaseAPIClass):
    @token_required("POST")
    def post(self, key):
        try:
            args = register_req.parse_args()
            email = args.get('email', "")
            username = args.get('username', "")
            
            if len(email) == 0 or len(username) == 0:
                raise CustomException("Email is invalid")
            
            admin = db.session.query(User).filter(User.id == key, User.role==User.Role.ADMIN).first()

            if admin == None:
                raise CustomException("You are not registered as admin, get lost!!!")
            else:
                user = db.session.query(User).filter(User.email == email, User.role!=User.Role.SUPPORT_STAFF).first()
                if user == None:
                    user = User(
                        email = email,
                        password = "FIRST_TIME",
                        username = username,
                        role = User.Role.SUPPORT_STAFF
                    )
                else:
                    user.role = User.Role.SUPPORT_STAFF

                db.session.add(user)
                db.session.commit()
                    
            self.message = "Support staff added successfully!"
            self.data = {}
        except CustomException as e:
            self.custom_code = 1005
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 1006
            self._exception_occured(e, False)
        return self._get_response()

class Logout(BaseAPIClass):
    @token_required("POST")
    def post(self, key):
        token = request.headers['Authorization']
        activeSession = db.session.query(ActiveSession).filter(
            ActiveSession.ver_code == token, ActiveSession.user_id == key
        ).first()

        if activeSession != None:
            db.session.delete(activeSession)
            db.session.commit()
        
        return self._get_response()
