from flask_restful import marshal, reqparse
from application.helpers import token_required, BaseAPIClass, CustomException, get_user
from application.database import db
from application.models.user import User
from application.models.tickets import FAQ, Tickets, TicketReplies
from application.response_fields import faq_output_with_response_fields

faq_req = reqparse.RequestParser()
faq_req.add_argument("title", required=True, type=str, trim=True, help='Title is required')
faq_req.add_argument("answer", required=True, type=str, trim=True, help='Answer is required')

edit_faq_req = reqparse.RequestParser()
edit_faq_req.add_argument("title", required=False, type=str, trim=True, store_missing="")
edit_faq_req.add_argument("answer", required=False, type=str, trim=True, store_missing="")
edit_faq_req.add_argument("faq_id", required=True, type=str, trim=True)

delete_faq_req = reqparse.RequestParser()
delete_faq_req.add_argument("faq_id", required=True, type=str, trim=True)

request_for_faq_args = reqparse.RequestParser()
request_for_faq_args.add_argument("ticket_id", required=True, type=str, trim=True)

req_faq_req = reqparse.RequestParser()
req_faq_req.add_argument("faq_id", required=True, type=str, trim=True)
req_faq_req.add_argument("rejected", required=False, type=int)

pin_req_args = reqparse.RequestParser()
pin_req_args.add_argument("ticket_id", required=True, type=str, trim=True)
pin_req_args.add_argument("pin", required=False, type=int, store_missing=0)

class FAQManagement(BaseAPIClass):

    def get(self):
        try:
            data = db.session.query(FAQ).filter(FAQ.status == FAQ.STATUS.ACTIVE).all()
            self.data = marshal(data, faq_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 5001
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5002
            self._exception_occured(e, False)
        return self._get_response()

    @token_required()
    def post(self, key):
        try:
            args = faq_req.parse_args()
            title = args.get('title', "")
            answer = args.get('answer', "")

            if len(title) >= 5000:
                raise CustomException("FAQ must be less than 5000")
            if len(answer) >= 5000:
                raise CustomException("Answer must be less than 5000")
            
            admin = get_user(key, admin=True)
            
            faq = FAQ(
                title=title,
                answer=answer,
                created_by_id = admin.id,
                approved_by_id = admin.id
            )
            db.session.add(faq)
            db.session.commit()
            
            self.message = "Successfully added the faq"
            self.data = marshal(faq, faq_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 5003
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5004
            self._exception_occured(e, False)
        return self._get_response()

    @token_required()
    def put(self, key):
        try:
            args = edit_faq_req.parse_args()
            title = args.get('title', "")
            answer = args.get('answer', "")
            faq_id = args.get('faq_id', "")

            if len(title) >= 5000:
                raise CustomException("FAQ must be less than 5000")
            if len(answer) >= 5000:
                raise CustomException("Answer must be less than 5000")
            
            admin = get_user(key, admin=False)

            if admin.role == User.Role.STUDENT:
                raise CustomException(("Permission denied", 403))
            
            faq = db.session.query(FAQ).filter(FAQ.id==faq_id, FAQ.created_by_id == admin.id, FAQ.status==FAQ.STATUS.ACTIVE).first()
            if faq is None:
                raise CustomException(("FAQ does not exist", 404))
            
            if len(title) > 0:
                faq.title = title
                
            if len(answer) > 0:
                faq.answer = answer
                
            db.session.add(faq)
            db.session.commit()
            
            self.message = "Successfully updated the faq"
            self.data = marshal(faq, faq_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 5005
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5006
            self._exception_occured(e, False)
        return self._get_response()

    @token_required()
    def delete(self, key):
        try:
            args = edit_faq_req.parse_args()
            faq_id = args.get('faq_id', "")

            admin = get_user(key, admin=True)

            print(admin)
            
            faq = db.session.query(FAQ).filter(FAQ.id==faq_id, FAQ.status==FAQ.STATUS.ACTIVE).first()
            if faq is None:
                raise CustomException(("FAQ does not exist", 404))
            
            faq.status = FAQ.STATUS.DELETED
            db.session.add(faq)
            db.session.commit()
            
            self.message = "Successfully deleted the faq"
        except CustomException as e:
            self.custom_code = 5007
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5008
            self._exception_occured(e, False)
        return self._get_response()

class FAQRequest(BaseAPIClass):

    @token_required()
    def post(self, key):
        try:
            args = request_for_faq_args.parse_args()
            ticket_id = args.get('ticket_id', "")

            user = get_user(key, admin=False)

            if user.role == User.Role.STUDENT:
                raise CustomException(("Permission denied", 403))

            ticket = db.session.query(Tickets).filter(Tickets.id == ticket_id, Tickets.status == Tickets.STATUS.ACTIVE).first()

            if ticket is None:
                raise CustomException(("Ticket does not exist", 404))
            
            answer = ticket.replies.filter(TicketReplies.is_answer == True, TicketReplies.status==TicketReplies.STATUS.ACTIVE).first()

            if answer is None:
                raise CustomException("Ticket is not resolved")
            
            already_faq = db.session.query(FAQ).filter(
                FAQ.ticket_id == ticket_id,
            ).first()

            if already_faq:
                raise CustomException("FAQ already requested")
            
            faq = FAQ(
                title=ticket.title,
                answer=answer.reply,
                created_by_id = user.id,
                status = FAQ.STATUS.REQUESTED,
                ticket_id = ticket.id
            )
            
            db.session.add(faq)
            db.session.commit()
            
            self.message = "Successfully requested for the faq"
            self.data = marshal(faq, faq_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 5009
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5010
            self._exception_occured(e, False)
        return self._get_response()

class FAQAccept(BaseAPIClass):
    @token_required("GET")
    def get(self, key):
        try:
            admin = get_user(key, admin=True)
            data = db.session.query(FAQ).filter((FAQ.status == FAQ.STATUS.REQUESTED) | (FAQ.status == FAQ.STATUS.DELETED)).all()
            self.data = marshal(data, faq_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 5011
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5012
            self._exception_occured(e, False)
        return self._get_response()
    
    @token_required()
    def post(self, key):
        try:
            args = req_faq_req.parse_args()
            faq_id = args.get('faq_id', "")
            rejected = args.get("rejected", 0)

            admin = get_user(key, admin=True)

            faq = db.session.query(FAQ).filter(FAQ.id==faq_id, (FAQ.status==FAQ.STATUS.REQUESTED) | (FAQ.status==FAQ.STATUS.DELETED)).first()
            if faq is None:
                raise CustomException(("FAQ does not exist", 404))
            
            if rejected == 1:
                faq.status = FAQ.STATUS.DELETED
            else:
                faq.status = FAQ.STATUS.ACTIVE

            faq.approved_by_id = admin.id

            db.session.add(faq)
            db.session.commit()
            
            self.message = "Successfully accepted for the faq"
            self.data = marshal(faq, faq_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 5013
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5014
            self._exception_occured(e, False)
        return self._get_response()

class PinTicket(BaseAPIClass):

    @token_required()
    def post(self, key):
        try:
            args = pin_req_args.parse_args()
            ticket_id = args.get('ticket_id', "")
            pin = args.get("pin", 0)

            user = get_user(key)

            if user.role == User.Role.STUDENT:
                raise CustomException(("Permission denied", 403))

            ticket = db.session.query(Tickets).filter(Tickets.id==ticket_id, Tickets.status==Tickets.STATUS.ACTIVE).first()
            if ticket is None:
                raise CustomException(("Ticket does not exist", 404))
            
            if pin == 1:
                ticket.priority = Tickets.PRIORITY.HIGH
            else:
                ticket.priority = Tickets.PRIORITY.LOW

            db.session.add(ticket)
            db.session.commit()
            
            self.message = "Successfully updated for the ticket"
            self.data = {}
        except CustomException as e:
            self.custom_code = 5015
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 5016
            self._exception_occured(e, False)
        return self._get_response()