from application.database import db
import uuid
from sqlalchemy.sql import func
from enum import Enum
from datetime import datetime

Base = db.Model

class User(Base):

    class Role(Enum):
        STUDENT = 1
        SUPPORT_STAFF = 2
        ADMIN = 3

    class ACCOUNT_STATUS(Enum):
        ACTIVE = 1
        BLOCKED = 2 
        DEACTIVATED = 3

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(1000), nullable=True)
    role = db.Column(db.Enum(Role), server_default="STUDENT")
    status = db.Column(db.Enum(ACCOUNT_STATUS), server_default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    
    #backref is a simple way to also declare a new property on the class
    tickets = db.relationship("Tickets", backref="tickets", lazy="dynamic")
    tags = db.relationship("SupportStaffTags", backref="support_staff_tags", lazy="dynamic")
