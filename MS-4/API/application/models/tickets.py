from application.database import db
import uuid
from sqlalchemy.sql import func
from enum import Enum
from datetime import datetime
from application.models.user import User

Base = db.Model

class Tickets(Base):
    __tablename__ = "tickets"

    class STATUS(Enum):
        ACTIVE = 1
        DELETED = 2

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    created_by_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    is_open = db.Column(db.Boolean(), default=True)
    is_offensive = db.Column(db.Boolean(), default=False)
    is_faq = db.Column(db.Boolean(), default=False)
    status = db.Column(db.Enum(STATUS), server_default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    
    #backref is a simple way to also declare a new property on the class
    replies = db.relationship("TicketReplies", backref="ticketreplies", lazy="dynamic")
    votes = db.relationship("TicketVotes", backref="ticketvotes", lazy="dynamic")
    tags = db.relationship("TicketTags", backref="tickettags", lazy="dynamic")

class TicketReplies(Base):
    __tablename__ = "ticketreplies"

    class STATUS(Enum):
        ACTIVE = 1
        DELETED = 2

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    reply = db.Column(db.String(5000), nullable=False)
    created_by_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    is_answer = db.Column(db.Boolean(), default=False)
    is_offensive = db.Column(db.Boolean(), default=False)
    reply_to = db.Column(db.Text, db.ForeignKey(Tickets.id, ondelete='CASCADE'), nullable=False)
    status = db.Column(db.Enum(STATUS), server_default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    
    votes = db.relationship("RepliesVotes", backref="repliesvotes", lazy="dynamic")

#Not making any mapping for relationship as can be both reply and ticket
class TicketFiles(Base):
    __tablename__ = "ticketfiles"

    class STATUS(Enum):
        ACTIVE = 1
        DELETED = 2

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = db.Column(db.String(5000), nullable=False)
    created_by_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    attached_to = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(STATUS), server_default="ACTIVE")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TicketVotes(Base):
    __tablename__ = "ticketvotes"
    
    class VOTE_TYPE(Enum):
        UP = 1
        DOWN = 2

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    ticket_id = db.Column(db.Text, db.ForeignKey(Tickets.id, ondelete='CASCADE'), nullable=False)
    vote = db.Column(db.Enum(VOTE_TYPE), server_default="UP")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    __table_args__ = (
        db.UniqueConstraint('user_id', 'ticket_id', name='_ticket_vote_uc'),
    )

class RepliesVotes(Base):
    __tablename__ = "repliesvotes"
    
    class VOTE_TYPE(Enum):
        UP = 1
        DOWN = 2

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    reply_id = db.Column(db.Text, db.ForeignKey(TicketReplies.id, ondelete='CASCADE'), nullable=False)
    vote = db.Column(db.Enum(VOTE_TYPE), server_default="UP")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())    

    __table_args__ = (
        db.UniqueConstraint('user_id', 'reply_id', name='_reply_vote_uc'),
    )

'''
TrackerEditTicket will keep track of tickets' or replies' edit call
old_obj and new_obj is the stringify version of it's json object
'''
class TrackerEditTicket(Base):
    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    old_obj = db.Column(db.String)
    new_obj = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    ticket_id = db.Column(db.Text, db.ForeignKey(Tickets.id, ondelete='CASCADE'), nullable=True)
    reply_id = db.Column(db.Text, db.ForeignKey(TicketReplies.id, ondelete='CASCADE'), nullable=True)

class Tags(Base):
    __tablename__ = "tags"
    
    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    tag_title = db.Column(db.String(200), unique=True, nullable=False)
    created_by_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

class TicketTags(Base):

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    tag_id = db.Column(db.Text, db.ForeignKey(Tags.id, ondelete='CASCADE'), nullable=False)
    ticket_id = db.Column(db.Text, db.ForeignKey(Tickets.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('tag_id', 'ticket_id', name='_ticket_vote_uc'),
    )

class SupportStaffTags(Base):
    __tablename__ = "support_staff_tags"

    id = db.Column(db.Text, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Text, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    tag_id = db.Column(db.Text, db.ForeignKey(Tags.id, ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    