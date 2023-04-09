from flask_restful import Resource, fields, marshal
from flask import request
from application.models.tickets import Tickets, TrackerEditTicket
from application.helpers import token_required, ResponseObj, get_user, CustomException, BaseAPIClass
from json import loads as json_loads, dumps
from application.database import db
from application.response_fields import ticket_output_with_response_fields

class TicketsAPI(BaseAPIClass):
    def _get_required(self, data, required_fields):
        for argument in required_fields:
            if argument not in data or not data[argument]:
                raise CustomException(f"{argument} not provided")
            
    @token_required("GET")
    def get(self):
        try:
            data = request.args

            required = ["ticket_id"]

            self._get_required(data, required)

            #We don't need user here
            # user = get_user(data["key"])

            ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"]).first()

            if not ticket:
                raise CustomException(("Ticket not found", 404))

            self.data = marshal(ticket, ticket_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 4001
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4002
            self._exception_occured(e, False)

        return self._get_response()

    @token_required()
    def post(self):
        try:
            data = json_loads(request.data)

            required = ["title", "description"]

            self._get_required(data, required)
            #We don't need user here
            # user = get_user(data["key"])
            
            ticket = Tickets(
                title = data["title"],
                description = data["description"],
                created_by_id = data["key"]
            )
            db.session.add(ticket)
            db.session.commit()

            self.data = marshal(ticket, ticket_output_with_response_fields)
    
        except CustomException as e:
            self.custom_code = 4003
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4004
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def put(self):
        try:
            data = json_loads(request.data)

            required = ["title", "description", "ticket_id"]

            self._get_required(data, required)

            user = get_user(data["key"])

            ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"]).first()

            oldObj = dumps(marshal(ticket, ticket_output_with_response_fields))

            if not ticket:
                raise CustomException(("Ticket not found", 404))
            
            if ticket.created_by_id != user.id:
                raise CustomException(("Forbidden to update this ticket", 403))
            
            if ticket.status == Tickets.STATUS.DELETED or ticket.is_offensive:
                raise CustomException(("Forbidden to update this ticket", 403))
            
            ticket.title = data["title"]
            ticket.description = data["description"]
            db.session.add(ticket)

            newObj = dumps(marshal(ticket, ticket_output_with_response_fields))

            trackerEdit = TrackerEditTicket(
                old_obj = oldObj,
                new_obj = newObj,
                user_id = data["key"],
                ticket_id = ticket.id
            )
            db.session.add(trackerEdit)

            db.session.commit()

            self.data = marshal(ticket, ticket_output_with_response_fields)

        except CustomException as e:
            self.custom_code = 4005
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4006
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def delete(self):
        try:
            data = json_loads(request.data)
            required = ["ticket_id"]
            self._get_required(data, required)

            user = get_user(data["key"])

            ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"]).first()

            if not ticket:
                raise CustomException(("Ticket not found", 404))
            
            if ticket.created_by_id != user.id:
                raise CustomException(("Forbidden to delete this ticket", 403))

            replies = ticket.replies.all()

            if len(replies) > 0:
                raise CustomException(("Forbidden to delete this ticket", 403))
            
            if ticket.status == Tickets.STATUS.DELETED:
                raise CustomException(("This ticket has been already deleted", 404))
            

            oldObj = dumps(marshal(ticket, ticket_output_with_response_fields))
            
            ticket.status = Tickets.STATUS.DELETED

            db.session.add(ticket)

            newObj = dumps(marshal(ticket, ticket_output_with_response_fields))

            trackerEdit = TrackerEditTicket(
                old_obj = oldObj,
                new_obj = newObj,
                user_id = data["key"],
                ticket_id = ticket.id
            )
            db.session.add(trackerEdit)

            db.session.commit()

        except CustomException as e:
            self.custom_code = 4007
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4008
            self._exception_occured(e, False)

        return self._get_response()