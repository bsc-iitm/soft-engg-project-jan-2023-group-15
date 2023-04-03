from flask_restful import Resource
from application.helpers import token_required, ResponseObj

class UserManagement(Resource):
    
    @token_required("GET")
    def get(self):
        return ResponseObj(success=False, message="Success", code=200, data={}, exceptionObj={}, custom_code=102)
    
    @token_required()
    def post(self):
        return ResponseObj(success=False, message="Success", code=200, data={}, exceptionObj={}, custom_code=103)