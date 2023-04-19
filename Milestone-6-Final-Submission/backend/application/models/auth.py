from application.database import db
from datetime import datetime
from application.models.user import User
import uuid

Base = db.Model

class ActiveSession(Base):
    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    ver_code = db.Column(db.String(1000), nullable=False)
    login_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    last_access_datetime = db.Column(db.DateTime, default=datetime.utcnow)