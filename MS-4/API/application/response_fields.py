from flask_restful import fields
from application.models.user import User
from application.models.tickets import Tickets, Tags, SupportStaffTags, TicketTags
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

ticket_output_with_response_fields = {
    "id" : fields.String,
    "title" : fields.String,
    "description" : fields.String,
    "created_by_id" : fields.String,
    "is_open" : fields.Boolean,
    "is_offensive" : fields.Boolean,
    "is_faq" : fields.Boolean,
    "status" : fields.String(attribute=lambda obj1: str(Tickets.STATUS(obj1.status).name)),
    "priority" : fields.String(attribute=lambda obj1: str(Tickets.PRIORITY(obj1.priority).name)),
    "created_at" : fields.DateTime,
    "last_updated_at" : fields.DateTime,
    "tags":fields.List(fields.Nested(ticket_tags), attribute=lambda obj: obj.tags.order_by(TicketTags.last_updated_at.desc()).all()),
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