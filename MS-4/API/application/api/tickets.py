from flask_restful import Resource, fields, marshal
from flask import request
from application.models.user import User
from application.models.tickets import Tickets, TrackerEditTicket
from application.helpers import token_required, ResponseObj
from json import loads as json_loads, dumps
from application.database import db

output_ticket = {
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
    "last_updated_at" : fields.DateTime
}

class TicketsAPI(Resource):
    @token_required("GET")
    def get(self):
        data = request.args

        required = ["ticket_id"]

        for argument in required:
            if argument not in data or not data[argument]:
                return ResponseObj(success=False, message=f"{argument} not provided", code=400, data={}, exceptionObj={}, custom_code=102)

        user = db.session.query(User).filter_by(id= data["key"]).first()

        if not user:
            return ResponseObj(success=False, message="User not found", code=404, data={}, exceptionObj={}, custom_code=103)
        
        ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"]).first()

        if not ticket:
            return ResponseObj(success=False, message="Ticket not found", code=404, data={}, exceptionObj={}, custom_code=103)

        return marshal(ticket, output_ticket), 200

    @token_required()
    def post(self):
        data = json_loads(request.data)

        required = ["title", "description"]

        for argument in required:
            if argument not in data or not data[argument]:
                return ResponseObj(success=False, message=f"{argument} not provided", code=400, data={}, exceptionObj={}, custom_code=102)

        user = db.session.query(User).filter_by(id= data["key"]).first()

        if not user:
            return ResponseObj(success=False, message="User not found", code=404, data={}, exceptionObj={}, custom_code=103)
        
        ticket = Tickets(
            title = data["title"],
            description = data["description"],
            created_by_id = data["key"]
        )
        db.session.add(ticket)
        db.session.commit()

        return marshal(ticket, output_ticket), 201
    
    @token_required()
    def put(self):
        data = json_loads(request.data)

        required = ["title", "description", "ticket_id"]

        for argument in required:
            if argument not in data or not data[argument]:
                return ResponseObj(success=False, message=f"{argument} not provided", code=400, data={}, exceptionObj={}, custom_code=102)

        user = db.session.query(User).filter_by(id= data["key"]).first()

        if not user:
            return ResponseObj(success=False, message="User not found", code=404, data={}, exceptionObj={}, custom_code=103)
        
        ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"]).first()

        oldObj = dumps(marshal(ticket, output_ticket))

        if not ticket:
            return ResponseObj(success=False, message="Ticket not found", code=404, data={}, exceptionObj={}, custom_code=103)
        
        if ticket.created_by_id != user.id:
            return ResponseObj(success=False, message="Forbidden to update this ticket", code=403, data={}, exceptionObj={}, custom_code=103)
        
        if ticket.status == Tickets.STATUS.DELETED or ticket.is_offensive:
            return ResponseObj(success=False, message="Forbidden to update this ticket", code=403, data={}, exceptionObj={}, custom_code=103)
        
        ticket.title = data["title"]
        ticket.description = data["description"]
        db.session.add(ticket)

        newObj = dumps(marshal(ticket, output_ticket))

        trackerEdit = TrackerEditTicket(
            old_obj = oldObj,
            new_obj = newObj,
            user_id = data["key"],
            ticket_id = ticket.id
        )
        db.session.add(trackerEdit)

        db.session.commit()

        return marshal(ticket, output_ticket), 201

    @token_required()
    def delete(self):
        data = json_loads(request.data)
        required = ["ticket_id"]

        for argument in required:
            if argument not in data or not data[argument]:
                return ResponseObj(success=False, message=f"{argument} not provided", code=400, data={}, exceptionObj={}, custom_code=102)

        user = db.session.query(User).filter_by(id= data["key"]).first()

        if not user:
            return ResponseObj(success=False, message="User not found", code=404, data={}, exceptionObj={}, custom_code=103)
        
        ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"]).first()

        if not ticket:
            return ResponseObj(success=False, message="Ticket not found", code=404, data={}, exceptionObj={}, custom_code=103)
        
        if ticket.created_by_id != user.id:
            return ResponseObj(success=False, message="Forbidden to delete this ticket", code=403, data={}, exceptionObj={}, custom_code=103)

        replies = ticket.replies.all()

        if len(replies) > 0:
            return ResponseObj(success=False, message="Forbidden to delete this ticket", code=403, data={}, exceptionObj={}, custom_code=103)
        
        if ticket.status == Tickets.STATUS.DELETED:
            return ResponseObj(success=False, message="This ticket has been already deleted", code=404, data={}, exceptionObj={}, custom_code=103)
        

        oldObj = dumps(marshal(ticket, output_ticket))
        
        ticket.status = Tickets.STATUS.DELETED

        db.session.add(ticket)

        newObj = dumps(marshal(ticket, output_ticket))

        trackerEdit = TrackerEditTicket(
            old_obj = oldObj,
            new_obj = newObj,
            user_id = data["key"],
            ticket_id = ticket.id
        )
        db.session.add(trackerEdit)

        db.session.commit()

        return "", 200