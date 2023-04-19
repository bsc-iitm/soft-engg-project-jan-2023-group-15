from __future__ import print_function

import base64
from email.mime.text import MIMEText
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SENDER_ADDRESS="iitm.online.afsdfdsf@gmail.com"
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']
CLIENT_SECRET_FILE = os.path.join(os.path.realpath(os.path.dirname(__file__)), "static", 'credentials.json')
APPLICATION_NAME = 'IITM BS Help Support'

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# create a message
def CreateMessage(to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: html text of the email message.

    Returns:
        An object containing a base64 encoded email object.
    """
    
    message = MIMEText(message_text, 'html')
    if type(to) == list:
        to = ", ".join(to)
    message['To'] = to
    message['From'] = APPLICATION_NAME
    message['Subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {
        'raw': encoded_message
    }
    print("Created message for: ", to)
    return create_message

#send message 
def SendMessage(service, user_id, message):
    """Send an email message.

    Args:
     service: Authorized Gmail API service instance.
     user_id: User's email address. The special value "me"
     can be used to indicate the authenticated user.
     message: Message to be sent.

    Returns:
     Sent Message.
    """
    try:
        send_message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(F'Message Id: {send_message["id"]}')
        return send_message
    except HttpError as error:
        print ('An error occurred: %s' % error)
        send_message = error
    return send_message

def email_send(to_address, subject, message):
    try:
        # Call the Gmail API
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds, cache_discovery=False)
        print("Sending email to: ", to_address)
        return SendMessage(service, 'me', CreateMessage(to_address, subject=subject, message_text=message))
    except HttpError as error:
        print(f'An error occurred: {error}')
        return error
