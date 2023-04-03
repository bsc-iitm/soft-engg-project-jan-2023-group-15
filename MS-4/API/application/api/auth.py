from flask_restful import Resource
from application.models.user import User
from application.database import db

class Login(Resource):

    def post(self):
        user = User(
            email = "dipak@patil3.com",
            password = "absccdd",
            username = "dipak",
            full_name = "dipak patil"
        )
        
        db.session.add(user)
        db.session.commit()
            
        user = User(
            email = "dipak@patil4.com",
            password = "absccdd",
            username = "dipak",
            full_name = "dipak patil"
        )
        db.session.add(user)
        db.session.commit()
        return {"success":True}, 200