from datetime import datetime, date, timedelta
from flask_restful import marshal
from pytz import timezone
from application.workers import celery
from celery.schedules import crontab
from application.database import db
from application.models.user import User
from application.models.tickets import Tickets, TicketReplies, TicketVotes
from application.helpers import format_message
from application.email import email_send
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
@celery.on_after_finalize.connect

def periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=0, hour=17), 
        daily_notification.s(), 
        name="daily notify admin"
    )

@celery.task()
def send_email(address, subject, file, data):
    email = email_send(
        to_address=address, 
        subject=subject, 
        message=format_message(file, data=data),
    )
    logger.info("Response from email_send" + str(email))
    logger.info("EMAIL SENT TO: " + str(address))
    return address

@celery.task()
def daily_notification():
    all_admins = db.session.query(User).filter(User.status == User.ACCOUNT_STATUS.ACTIVE, User.role == User.Role.ADMIN).all()
    today = date.today()
    last_2_days = today - timedelta(days=2)
    unresponsed_tickets = db.session.query(Tickets).join(TicketReplies).filter(
        Tickets.status == Tickets.STATUS.ACTIVE, 
        Tickets.last_updated_at <= last_2_days,
    ).all()
    final_unresponsed_tickets = []
    for ticket in unresponsed_tickets:
        if(ticket.replies.filter(
            TicketReplies.status == TicketReplies.STATUS.ACTIVE, 
            TicketReplies.is_answer == True
        ).count() == 0):
            final_unresponsed_tickets.append(ticket)
    print(unresponsed_tickets, all_admins)
    if len(final_unresponsed_tickets) > 0:
        send_email.apply_async(args=[
            [admin.email for admin in all_admins],
            "Tickets that have not been responded to in the last 2 days",
            "daily_notification.html",
            {
                "tickets":final_unresponsed_tickets
            }
        ])
    return "Done" + str(len(final_unresponsed_tickets))

@celery.task()
def notify_user(ticket_id, key):
    ticket = db.session.query(Tickets).filter(
        Tickets.id == ticket_id,
        Tickets.status==Tickets.STATUS.ACTIVE
    ).first()
    if ticket == None:
        return "Ticket does not exist"
    if ticket:
        reply = ticket.replies.filter(TicketReplies.status == TicketReplies.STATUS.ACTIVE).order_by(TicketReplies.created_at.desc()).first()
        votes = ticket.votes.filter(TicketVotes.vote == TicketVotes.VOTE_TYPE.UP).all()
        user_ids = [vote.user_id for vote in votes if vote.user_id != key]
        user_ids.append(ticket.created_by_id)
        users = db.session.query(User).filter(User.id.in_(user_ids)).all()
        send_email.apply_async(args=[
            list(set([user.email for user in users])),
            "Update on ticket",
            "ticket_responded.html",
            {
                "ticket":ticket,
                "reply":reply,
            }
        ])
    return "Done"