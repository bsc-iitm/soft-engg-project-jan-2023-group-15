from flask_restful import marshal, reqparse
from application.helpers import token_required, BaseAPIClass, CustomException, get_user
from application.database import db
from application.models.user import User
from application.models.auth import ActiveSession
from application.response_fields import user_output_with_response_fields, staff_output_with_response_fields

edit_profile_req = reqparse.RequestParser()
edit_profile_req.add_argument("username", required=False, type=str, trim=True, help='Username is required')
edit_profile_req.add_argument("full_name", required=False, type=str, trim=True, help='Full Name is required')

blocked_profile_req = reqparse.RequestParser()
blocked_profile_req.add_argument("user_id", required=False, type=str, trim=True, help='User is required')

class UserManagement(BaseAPIClass):
    
    @token_required("GET")
    def get(self, key):
        try:
            user = get_user(key)
            if user.role == User.Role.SUPPORT_STAFF:
                self.data = marshal(user, staff_output_with_response_fields)
            else:
                self.data = marshal(user, user_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 2001
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 2002
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def post(self, key):
        try:
            args = edit_profile_req.parse_args()
            username = args.get('username', "")
            full_name = args.get('full_name', "")
            if full_name is None and username is None:
                raise CustomException("Username or full name is required to edit")
            
            user = get_user(key)
            if username != None and len(username) > 0:
                user.username = username
            if full_name != None and len(full_name) > 0:
                user.full_name = full_name
            
            db.session.add(user)
            db.session.commit()

            self.data = marshal(user, user_output_with_response_fields)

        except CustomException as e:
            self.custom_code = 2003
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 2004
            self._exception_occured(e, False)

        return self._get_response()

class BlockedUser(BaseAPIClass):
    def _remove_session(self, key):
        delete_q = ActiveSession.__table__.delete().where(ActiveSession.user_id == key)
        db.session.execute(delete_q)
        db.session.commit()

    @token_required()
    def post(self, key):
        try:
            user = get_user(key)
            if user.role == User.Role.STUDENT:
                raise CustomException("Permission denied")
            args = blocked_profile_req.parse_args()
            user_id =  args.get('user_id', "")
            user_to_block = get_user(user_id)
            user_to_block.status = User.ACCOUNT_STATUS.BLOCKED
            db.session.add(user_to_block)
            db.session.commit()
            self._remove_session(user_id)
            self.message = f"Successfully blocked {user_to_block.username}"
        except CustomException as e:
            self.custom_code = 2005
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 2006
            self._exception_occured(e, False)

        return self._get_response()
class DeactivateUser(BlockedUser):

    @token_required()
    def post(self, key):
        try:
            user = get_user(key)
            user.status = User.ACCOUNT_STATUS.DEACTIVATED
            db.session.add(user)
            db.session.commit()
            self._remove_session(key)
        except CustomException as e:
            self.custom_code = 2005
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 2006
            self._exception_occured(e, False)
            
        return self._get_response()

class UnblockedUser(BaseAPIClass):
    @token_required()
    def post(self, key):
        try:
            user = get_user(key)
            if user.role == User.Role.STUDENT:
                raise CustomException("Permission denied")
            args = blocked_profile_req.parse_args()
            user_id =  args.get('user_id', "")
            user_to_unblock = get_user(user_id, isActive=False)
            if user_to_unblock.status == User.ACCOUNT_STATUS.BLOCKED:
                user_to_unblock.status = User.ACCOUNT_STATUS.ACTIVE
                db.session.add(user_to_unblock)
                db.session.commit()
                self.message = f"Successfully unblocked {user_to_unblock.username}"
        except CustomException as e:
            self.custom_code = 2007
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 2008
            self._exception_occured(e, False)

        return self._get_response()

class GetSupportStaff(BaseAPIClass):
    
    @token_required("GET")
    def get(self, key):
        try:
            user = get_user(key, admin=True)
            staff = db.session.query(User).filter(User.role == User.Role.SUPPORT_STAFF).all()
            self.data = marshal(staff, staff_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 2009
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 2010
            self._exception_occured(e, False)

        return self._get_response()
    