from flask_restful import fields
from application.models.user import User
from application.models.tickets import Tickets, Tags, SupportStaffTags, TicketTags, FAQ, TicketReplies, TicketFiles, TicketVotes, RepliesVotes
from application.database import db

user_output_with_response_fields = {
    "id": fields.String,
    "username": fields.String,
    "email": fields.String,
    "full_name": fields.String,
    "profile_picture": fields.String,
    "role": fields.String(attribute=lambda obj: str(User.Role(obj.role).name)),
    "created_at":fields.DateTime,
    "last_updated_at":fields.DateTime,
}

tag_output_with_response_fields = {
    "id" : fields.String,
    "tag_title" : fields.String,
    "created_by_id" : fields.String,
    "status" : fields.String(attribute=lambda obj1: str(Tags.STATUS(obj1.status).name)),
    "created_at" : fields.DateTime,
    "last_updated_at" : fields.DateTime
}

ticket_tags = {
    "id" : fields.String,
    "ticket_id" : fields.String,
    "tag_id" : fields.String,
    "created_at" : fields.DateTime,
    "tag": fields.Nested(tag_output_with_response_fields, attribute=lambda obj: db.session.query(Tags).filter(Tags.id==obj.tag_id).first()),
}

file_output_with_response_fields = {
    "id" : fields.String,
    "url" : fields.String,
    "created_by_id" : fields.String,
    "attached_to" : fields.String,
    "created_at" : fields.DateTime,
    "status": fields.String(attribute=lambda obj1: str(TicketFiles.STATUS(obj1.status).name)),
}

reply_output_with_response_fields = {
    "id" : fields.String,
    "reply" : fields.String,
    "created_by_id" : fields.String,
    "created_by_user": fields.Nested(user_output_with_response_fields, attribute=lambda obj: db.session.query(User).filter(User.id==obj.created_by_id).first()),
    "is_answer" : fields.Boolean,
    "is_offensive": fields.Boolean,
    "created_at" : fields.DateTime,
    "reply_to": fields.String,
    "last_updated_at": fields.DateTime,
    "status": fields.String(attribute=lambda obj1: str(TicketReplies.STATUS(obj1.status).name)),
    "files":fields.List(fields.Nested(file_output_with_response_fields), attribute=lambda obj: db.session.query(TicketFiles).filter(TicketFiles.attached_to == obj.id).order_by(TicketFiles.created_at.desc()).all()),
    "votes":{
        "upvotes":fields.Integer(attribute=lambda obj: obj.votes.filter(RepliesVotes.vote == RepliesVotes.VOTE_TYPE.UP).count()),
        "downvotes":fields.Integer(attribute=lambda obj: obj.votes.filter(RepliesVotes.vote == RepliesVotes.VOTE_TYPE.DOWN).count()),
    }
}


ticket_output_with_response_fields = {
    "id" : fields.String,
    "title" : fields.String,
    "description" : fields.String,
    "created_by_id" : fields.String,
    "created_by_user": fields.Nested(user_output_with_response_fields, attribute=lambda obj: db.session.query(User).filter(User.id==obj.created_by_id).first()),
    "is_open" : fields.Boolean,
    "is_offensive" : fields.Boolean,
    "status" : fields.String(attribute=lambda obj1: str(Tickets.STATUS(obj1.status).name)),
    "priority" : fields.String(attribute=lambda obj1: str(Tickets.PRIORITY(obj1.priority).name)),
    "created_at" : fields.DateTime,
    "last_updated_at" : fields.DateTime,
    "tags":fields.List(fields.Nested(ticket_tags), attribute=lambda obj: obj.tags.order_by(TicketTags.created_at.desc()).all()),
    "files":fields.List(fields.Nested(file_output_with_response_fields), attribute=lambda obj: db.session.query(TicketFiles).filter(TicketFiles.attached_to == obj.id).order_by(TicketFiles.created_at.desc()).all()),
    "replies":fields.List(fields.Nested(reply_output_with_response_fields), attribute=lambda obj: obj.replies.filter(TicketReplies.status == TicketReplies.STATUS.ACTIVE).order_by(TicketReplies.created_at.desc()).all()),
    "votes":{
        "upvotes":fields.Integer(attribute=lambda obj: obj.votes.filter(TicketVotes.vote == TicketVotes.VOTE_TYPE.UP).count()),
        "downvotes":fields.Integer(attribute=lambda obj: obj.votes.filter(TicketVotes.vote == TicketVotes.VOTE_TYPE.DOWN).count()),
    }
}

ticket_all_output_with_response_fields = {
    "id" : fields.String,
    "title" : fields.String,
    "description" : fields.String,
    "created_by_id" : fields.String,
    "created_by_user": fields.Nested(user_output_with_response_fields, attribute=lambda obj: db.session.query(User).filter(User.id==obj.created_by_id).first()),
    "is_open" : fields.Boolean,
    "is_offensive" : fields.Boolean,
    "status" : fields.String(attribute=lambda obj1: str(Tickets.STATUS(obj1.status).name)),
    "priority" : fields.String(attribute=lambda obj1: str(Tickets.PRIORITY(obj1.priority).name)),
    "created_at" : fields.DateTime,
    "last_updated_at" : fields.DateTime,
    "tags":fields.List(fields.Nested(ticket_tags), attribute=lambda obj: obj.tags.order_by(TicketTags.created_at.desc()).all()),
    "votes":{
        "upvotes":fields.Integer(attribute=lambda obj: obj.votes.filter(TicketVotes.vote == TicketVotes.VOTE_TYPE.UP).count()),
        "downvotes":fields.Integer(attribute=lambda obj: obj.votes.filter(TicketVotes.vote == TicketVotes.VOTE_TYPE.DOWN).count()),
    }
}

staff_tags = {
    "id" : fields.String,
    "user_id" : fields.String,
    "tag_id" : fields.String,
    "created_by_id" : fields.String,
    "status" : fields.String(attribute=lambda obj1: str(SupportStaffTags.STATUS(obj1.status).name)),
    "created_at" : fields.DateTime,
    "last_updated_at" : fields.DateTime,
    "tag": fields.Nested(tag_output_with_response_fields, attribute=lambda obj: db.session.query(Tags).filter(Tags.id==obj.tag_id).first()),
}

staff_output_with_response_fields= {
    **user_output_with_response_fields,
    "tags":fields.List(fields.Nested(staff_tags), attribute=lambda obj: obj.tags.filter(SupportStaffTags.status == SupportStaffTags.STATUS.ACTIVE).order_by(SupportStaffTags.last_updated_at.desc()).all()),
}

faq_output_with_response_fields = {
    "id" : fields.String,
    "title" : fields.String,
    "answer" : fields.String,
    "status" : fields.String(attribute=lambda obj1: str(FAQ.STATUS(obj1.status).name)),
    "created_at" : fields.DateTime,
    "last_updated_at" : fields.DateTime,
}