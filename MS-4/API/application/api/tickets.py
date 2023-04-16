from flask_restful import Resource, fields, marshal, reqparse
from flask import request
from application.models.user import User
from application.models.tickets import Tickets, TrackerEditTicket, Tags, TicketTags, TicketFiles, TicketVotes, TicketReplies, RepliesVotes, SupportStaffTickets
from application.helpers import token_required, ResponseObj, get_user, CustomException, BaseAPIClass
from json import loads as json_loads, dumps
from application.database import db
from application.response_fields import ticket_output_with_response_fields, ticket_all_output_with_response_fields, reply_output_with_response_fields
from application.tasks import notify_user

tickets_all_args = reqparse.RequestParser()
tickets_all_args.add_argument("filters", required=True, type=list, trim=True, store_missing=[])

tickets_files_delete_args = reqparse.RequestParser()
tickets_files_delete_args.add_argument("file_ids", required=True, type=list, trim=True, store_missing=[])

ticket_vote_args = reqparse.RequestParser()
ticket_vote_args.add_argument("vote", required=True, type=int, trim=True, store_missing=1)
ticket_vote_args.add_argument("ticket_id", required=False, type=str, trim=True, store_missing="")
ticket_vote_args.add_argument("reply_id", required=False, type=str, trim=True, store_missing="")

reply_to_ticket_args = reqparse.RequestParser()
reply_to_ticket_args.add_argument("ticket_id", required=True, type=str, trim=True, store_missing="")
reply_to_ticket_args.add_argument("reply", required=True, type=str, trim=True, store_missing="")
reply_to_ticket_args.add_argument("reply_files", required=False, type=list, trim=True, store_missing=[])

edit_reply_to_ticket_args = reqparse.RequestParser()
edit_reply_to_ticket_args.add_argument("reply_id", required=True, type=str, trim=True, store_missing="")
edit_reply_to_ticket_args.add_argument("reply", required=False, type=str, trim=True, store_missing="")
edit_reply_to_ticket_args.add_argument("reply_files", required=True, type=list, trim=True, store_missing=[])

delete_reply_req_args = reqparse.RequestParser()
delete_reply_req_args.add_argument("reply_id", required=True, type=str, trim=True, store_missing="")

edit_status_req_args = reqparse.RequestParser()
edit_status_req_args.add_argument("ticket_id", required=False, type=str, trim=True, store_missing="")
edit_status_req_args.add_argument("is_open", required=False, type=int, trim=True, store_missing=-1)
edit_status_req_args.add_argument("is_offensive", required=False, type=int, trim=True, store_missing=-1)
edit_status_req_args.add_argument("is_answer", required=False, type=int, trim=True, store_missing=-1)
edit_status_req_args.add_argument("reply_id", required=False, type=str, trim=True, store_missing="")

assign_ticket_req_args = reqparse.RequestParser()
assign_ticket_req_args.add_argument("ticket_id", required=True, type=str, trim=True, store_missing="")
assign_ticket_req_args.add_argument("user_id", required=True, type=str, trim=True, store_missing="")

class TicketsAPI(BaseAPIClass):
    def _get_required(self, data, required_fields):
        for argument in required_fields:
            if argument not in data or not data[argument]:
                raise CustomException(f"{argument} not provided")

    @token_required("GET")
    def get(self, key):
        try:
            data = request.args

            required = ["ticket_id"]

            self._get_required(data, required)

            #We don't need user here
            # user = get_user(data["key"])

            ticket = db.session.query(Tickets).filter_by(id= data["ticket_id"], status=Tickets.STATUS.ACTIVE).first()

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
    def post(self, key):
        try:
            data = json_loads(request.data)

            required = ["title", "description", 'tags', 'files']

            self._get_required(data, required)
            #We don't need user here
            user = get_user(key)

            tags = data['tags']
            files = data['files']

            if not isinstance(tags, list):
                raise CustomException(("Tags provided should be in list", 400))
            
            if len(tags) <= 0:
                raise CustomException(("At least one tag should be in list", 400))
            
            if not isinstance(files, list):
                raise CustomException(("Files provided should be in list", 400))
            
            ticket_tags = db.session.query(Tags).filter(Tags.id.in_(tags), Tags.status==Tags.STATUS.ACTIVE).all()
            
            if len(ticket_tags) != len(tags):
                raise CustomException(("Some tags are not valid", 400))

            ticket = Tickets(
                title = data["title"],
                description = data["description"],
                created_by_id = data["key"]
            )
            db.session.add(ticket)
            db.session.commit()

            #print(ticket.id)
            objects = []

            for tag_id in tags:
                ticket_tag = TicketTags(tag_id= tag_id, ticket_id= ticket.id)
                objects.append(ticket_tag)

            db.session.add_all(objects)
            db.session.commit()

            file_objects = []

            for file in files:
                ticket_file = TicketFiles(
                    url = file,
                    created_by_id = user.id,
                    attached_to = ticket.id
                )
                file_objects.append(ticket_file)

            db.session.add_all(file_objects)
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
    def put(self, key):
        try:
            data = json_loads(request.data)

            required = ["title", "description", "ticket_id", 'tags', 'files']

            self._get_required(data, required)

            user = get_user(key)

            tags = data["tags"]
            files = data['files']

            if not isinstance(tags, list):
                raise CustomException(("Tags provided should be in list", 400))
            if len(tags) <= 0:
                raise CustomException(("At least one tag should be in list", 400))
            
            if not isinstance(files, list):
                raise CustomException(("Files provided should be in list", 400))
            
            # for tag_id in :
            ticket_tags = db.session.query(Tags).filter(Tags.id.in_(tags), Tags.status==Tags.STATUS.ACTIVE).all()
            
            if len(ticket_tags) != len(tags):
                raise CustomException(("Some tags are not valid", 400))

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

            prev_tags = ticket.tags.all()

            for tag in prev_tags:
                t_id = tag.id
                if t_id not in tags:
                    db.session.delete(tag)

            for tag_id in tags:
                t = db.session.query(TicketTags).filter(TicketTags.tag_id == tag_id, TicketTags.ticket_id == ticket.id).first()
                if not t:
                    t = TicketTags(tag_id= tag_id, ticket_id= ticket.id)
                    db.session.add(t)
                
            file_objects = []

            for file in files:
                ticket_file = TicketFiles(
                    url = file,
                    created_by_id = user.id,
                    attached_to = ticket.id
                )
                file_objects.append(ticket_file)

            db.session.add_all(file_objects)
            db.session.commit()

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
    def delete(self, key):
        try:
            data = json_loads(request.data)
            required = ["ticket_id"]
            self._get_required(data, required)

            user = get_user(key)

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

class TicketsAll(BaseAPIClass):

    @token_required("GET")
    def get(self, key):
        try:
            args = tickets_all_args.parse_args()
            filters = args.get('filters', [])
            
            tickets = db.session.query(Tickets).filter(
                Tickets.status==Tickets.STATUS.ACTIVE, 
                Tickets.tags.in_(filters)
            ).order_by(Tickets.priority.desc(), Tickets.last_updated_at.desc()).all()

            self.data = marshal(tickets, ticket_all_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 4009
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4010
            self._exception_occured(e, False)

        return self._get_response()

class TicketsStaffAll(BaseAPIClass):

    @token_required("GET")
    def get(self, key):
        try:
            user = get_user(key)

            if user.role != User.ROLE.STAFF:
                raise CustomException(("Forbidden to access this route", 403))
            
            tags = user.tags.filter(Tags.status==Tags.STATUS.ACTIVE).all()

            tickets_tags = db.session.query(Tickets).filter(
                Tickets.status==Tickets.STATUS.ACTIVE, 
                Tickets.tags.in_(tags)
            ).order_by(Tickets.priority.desc(), Tickets.last_updated_at.desc()).all()
            
            support_staff = db.session.query(SupportStaffTickets).filter(
                SupportStaffTickets.user_id == user.id,
                SupportStaffTickets.status == SupportStaffTickets.STATUS.ACTIVE
            )
            
            assigned_tickets = db.session.query(Tickets).filter(
                Tickets.status==Tickets.STATUS.ACTIVE,
                Tickets.id.in_(support_staff)
            ).order_by(Tickets.priority.desc(), Tickets.last_updated_at.desc()).all()

            self.data = {
                "tags_tickets":marshal(tickets_tags, ticket_all_output_with_response_fields),
                "assigned_tickets":marshal(assigned_tickets, ticket_all_output_with_response_fields)
            }

        except CustomException as e:
            self.custom_code = 4009
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4010
            self._exception_occured(e, False)

        return self._get_response()

class TicketsFilesDelete(BaseAPIClass):

    @token_required()
    def post(self, key):
        try:
            args = tickets_files_delete_args.parse_args()
            file_ids = args.get('file_ids', [])

            if len(file_ids) == 0:
                raise CustomException(("No files to delete", 400))
            
            user = get_user(key)
            
            files = db.session.query(TicketFiles).filter(
                Tickets.id.in_(file_ids),
                created_by_id = user.id
            ).all()

            if len(files) == 0:
                raise CustomException(("No files to delete", 400))

            for file in files:
                file.status = TicketFiles.STATUS.DELETED
                db.session.add(file)
            
            db.session.commit()

            self.data = {}
        except CustomException as e:
            self.custom_code = 4011
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4012
            self._exception_occured(e, False)

        return self._get_response()

class TicketsUpDownVote(BaseAPIClass):
    
    @token_required("GET")
    def post(self, key):
        try:
            args = ticket_vote_args.parse_args()
            vote = args.get('vote', 1)
            ticket_id = args.get('ticket_id', '')
            reply_id = args.get('reply_id', '')

            user = get_user(key)

            if len(ticket_id) == 0 and len(reply_id) == 0:
                raise CustomException(("Invalid request", 400))

            if len(ticket_id) > 0:
                ticket = db.session.query(Tickets).filter_by(id=ticket_id, status=Tickets.STATUS.ACTIVE).first()
                if not ticket:
                    raise CustomException(("Ticket not found", 404))
                
                already_voted = db.session.query(TicketVotes).filter_by(user_id = user.id, ticket_id = ticket_id).first()
                
             
                if vote == 1:
                    vote = TicketVotes.VOTE_TYPE.UP
                elif vote == -1:
                    vote = TicketVotes.VOTE_TYPE.DOWN
                else:
                    raise CustomException(("Invalid vote", 400))
                
                if already_voted and already_voted.vote != vote:
                    already_voted.vote = vote
                    db.session.add(already_voted)
                    db.session.commit()
                else:
                    ticketVote = TicketVotes(
                        user_id = user.id,
                        ticket_id = ticket.id,
                        vote = vote
                    )
                    db.session.add(ticketVote)
                    db.session.commit()

            elif len(reply_id) > 0:
                reply = db.session.query(TicketReplies).filter_by(id=reply_id, status=TicketReplies.STATUS.ACTIVE).first()
                if not reply:
                    raise CustomException(("Reply not found", 404))
                
                already_voted = db.session.query(RepliesVotes).filter_by(user_id = user.id, reply_id = reply_id).first()
                
                if vote == 1:
                    vote = RepliesVotes.VOTE_TYPE.UP
                elif vote == -1:
                    vote = RepliesVotes.VOTE_TYPE.DOWN
                else:
                    raise CustomException(("Invalid vote", 400))
                
                if already_voted and already_voted.vote != vote:
                    already_voted.vote = vote
                    db.session.add(already_voted)
                    db.session.commit()
                else:
                    ticketVote = RepliesVotes(
                        user_id = user.id,
                        reply_id = reply.id,
                        vote = vote
                    )
                    db.session.add(ticketVote)
                    db.session.commit()
                
            else:
                raise CustomException(("Invalid request", 400))
            
            self.data = {}
        except CustomException as e:
            self.custom_code = 4013
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4014
            self._exception_occured(e, False)

        return self._get_response()

class ReplyToTicket(BaseAPIClass):

    @token_required()
    def post(self, key):
        try:
            args = reply_to_ticket_args.parse_args()
            ticket_id = args.get('ticket_id', '')
            reply = args.get('reply', '')
            files = args.get('files', [])

            if len(ticket_id) == 0 or len(reply) == 0:
                raise CustomException(("Invalid request", 400))
            
            user = get_user(key)
            reply_ticket = TicketReplies(
                reply = reply,
                created_by_id = user.id,
                reply_to = ticket_id
            )
            db.session.add(reply_ticket)
            db.session.commit()

            file_objects = []

            for file in files:
                ticket_file = TicketFiles(
                    url = file,
                    created_by_id = user.id,
                    attached_to = reply.id
                )
                file_objects.append(ticket_file)

            db.session.add_all(file_objects)
            db.session.commit()

            notify_user.apply_async(args=[reply_ticket.id])

        except CustomException as e:
            self.custom_code = 4017
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4018
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def put(self, key):
        try:
            args = edit_reply_to_ticket_args.parse_args()
            reply_id = args.get('reply_id', '')
            reply = args.get('reply', '')
            files = args.get('files', [])

            if len(reply_id) == 0 and (len(reply) == 0 or len(files) == 0):
                raise CustomException(("Invalid request", 400))
            
            user = get_user(key)

            reply_ticket = db.session.query(TicketReplies).filter_by(id=reply_id, status=TicketReplies.STATUS.ACTIVE).first()
            
            if not reply_ticket:
                raise CustomException(("Reply not found", 404))
            
            if len(reply_ticket) > 0:
                reply_ticket.reply = reply
                db.session.add(reply_ticket)
                db.session.commit()

            if len(files) > 0:
                file_objects = []

                for file in files:
                    ticket_file = TicketFiles(
                        url = file,
                        created_by_id = user.id,
                        attached_to = reply_ticket.id
                    )
                    file_objects.append(ticket_file)

                db.session.add_all(file_objects)
                db.session.commit()

            notify_user.apply_async(args=[reply_ticket.reply_to])

            self.data = marshal(reply, reply_output_with_response_fields)
        except CustomException as e:
            self.custom_code = 4019
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4020
            self._exception_occured(e, False)

        return self._get_response()
    
    @token_required()
    def delete(self, key):
        try:
            args = delete_reply_req_args.parse_args()
            reply_id = args.get('reply_id', '')

            if len(reply_id) == 0:
                raise CustomException(("Invalid request", 400))
            
            user = get_user(key)

            reply_ticket = db.session.query(TicketReplies).filter_by(id=reply_id, created_by_id=user.id, status=TicketReplies.STATUS.ACTIVE).first()
            
            if not reply_ticket:
                raise CustomException(("Reply not found", 404))
            
            reply_ticket.status = TicketReplies.STATUS.DELETED
            db.session.add(reply_ticket)
            db.session.commit()

            self.data = {}
        except CustomException as e:
            self.custom_code = 4023
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4024
            self._exception_occured(e, False)

        return self._get_response()

class EditStatusTicket(BaseAPIClass):

    @token_required()
    def post(self, key):
        try:
            args = edit_status_req_args.parse_args()
            ticket_id = args.get('ticket_id', '')
            reply_id = args.get('reply_id', '')
            is_open = args.get('is_open', -1)
            is_answer = args.get('is_answer', -1)
            is_offensive = args.get('is_offensive', -1)

            if len(ticket_id) == 0 and len(reply_id) == 0:
                raise CustomException(("Invalid request", 400))
            
            user = get_user(key)

            if user.role == User.Role.STUDENT:
                raise CustomException(("You are not allowed to perform this action", 403))
            
            if len(ticket_id) > 0:
                ticket = db.session.query(Tickets).filter_by(id=ticket_id, status=Tickets.STATUS.ACTIVE).first()
                
                if not ticket:
                    raise CustomException(("Ticket not found", 404))

                oldObj = dumps(marshal(ticket, ticket_all_output_with_response_fields))

                if is_open != -1:
                    if is_open == 0:
                        ticket.is_open = False
                    else:
                        ticket.is_open = True
                        
                if is_offensive != -1:
                    if is_offensive == 0:
                        ticket.is_offensive = False
                    else:
                        ticket.is_offensive = True
                        
                db.session.add(ticket)
                db.session.commit()
                    
                newObj = dumps(marshal(ticket, ticket_all_output_with_response_fields))

                trackerEdit = TrackerEditTicket(
                    old_obj = oldObj,
                    new_obj = newObj,
                    user_id = user.id,
                    ticket_id = ticket.id
                )
                db.session.add(trackerEdit)

                db.session.commit()
            elif len(reply_id) > 0:
                reply = db.session.query(TicketReplies).filter_by(id=reply_id, status=TicketReplies.STATUS.ACTIVE).first()
                
                if not reply:
                    raise CustomException(("Reply not found", 404))

                if is_answer != -1:
                    if is_answer == 0:
                        reply.is_answer = False
                    else:
                        already_answer = db.session.query(TicketReplies).filter_by(reply_to=reply.reply_to, is_answer=True, status=TicketReplies.STATUS.ACTIVE).first()
                        if already_answer:
                            already_answer.is_answer = False
                            db.session.add(already_answer)
                            db.session.commit()
                        reply.is_answer = True
                        notify_user.apply_async(args=[reply.reply_to])
                if is_offensive != -1:
                    if is_offensive == 0:
                        reply.is_offensive = False
                    else:
                        reply.is_offensive = True

                db.session.add(reply)
                db.session.commit()
        
        except CustomException as e:
            self.custom_code = 4017
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4018
            self._exception_occured(e, False)

        return self._get_response()

class AssignTicket(BaseAPIClass):

    @token_required()
    def post(self, key):
        try:
            args = assign_ticket_req_args.parse_args()
            ticket_id = args.get('ticket_id', '')
            user_id = args.get('user_id', '')

            if len(ticket_id) == 0 and len(user_id) == 0:
                raise CustomException(("Invalid request", 400))
            
            admin = get_user(key, admin=True)
            user = get_user(user_id)

            ticket = db.session.query(Tickets).filter_by(id=ticket_id, status=Tickets.STATUS.ACTIVE).first()
            
            if not ticket:
                raise CustomException(("Ticket not found", 404))

            already_assigned = db.session.query(SupportStaffTickets).filter_by(
                user_id = user.id, 
                ticket_id=ticket.id, 
                status=SupportStaffTickets.STATUS.ACTIVE
            ).first()

            if already_assigned:
                raise CustomException(("User already assigned to this ticket", 400))
            
            new_assign = SupportStaffTickets(
                user_id = user.id,
                ticket_id = ticket.id,
                created_by_id = admin.id
            )

            db.session.add(new_assign)
            db.session.commit()

            self.data = {}

        except CustomException as e:
            self.custom_code = 4019
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4020
            self._exception_occured(e, False)

        return self._get_response()

    @token_required()
    def delete(self, key):
        try:
            args = assign_ticket_req_args.parse_args()
            ticket_id = args.get('ticket_id', '')
            user_id = args.get('user_id', '')

            if len(ticket_id) == 0 and len(user_id) == 0:
                raise CustomException(("Invalid request", 400))
            
            admin = get_user(key, admin=True)
            user = get_user(user_id)

            ticket = db.session.query(Tickets).filter_by(id=ticket_id, status=Tickets.STATUS.ACTIVE).first()
            
            if not ticket:
                raise CustomException(("Ticket not found", 404))

            already_assigned = db.session.query(SupportStaffTickets).filter_by(
                user_id = user.id, 
                ticket_id=ticket.id, 
                status=SupportStaffTickets.STATUS.ACTIVE
            ).first()

            if not already_assigned:
                raise CustomException(("User is not assigned to this ticket", 400))
            
            already_assigned.status = SupportStaffTickets.STATUS.DELETED
            db.session.add(already_assigned)
            db.session.commit()

            self.data = {}

        except CustomException as e:
            self.custom_code = 4021
            self._exception_occured(e, True)
        except Exception as e:
            self.custom_code = 4022
            self._exception_occured(e, False)

        return self._get_response()