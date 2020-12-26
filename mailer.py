# Mailer implements basic emailing, using the SMTP protcol. 
# To avoid having your email getting sent to junk, format the 
# email properly or email yourself.

# TODO: 
# - log instead of printing errors and results

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# For SSL
PORT = 587  

# The sender in this case can only be a Gmail account.
# The senders Gmail account also needs to allow third party 
# services for SMTP to work.
SMTP_SERVER = "smtp.gmail.com" 

def build_message(sender_email, recipient_email, subject, body):
    """
    Builds an email message using MIMEMultipart.

    Parameters:
        sender_email (string): the senders email (from).
        recipient_email (string): the recipient email (to).
        subject (string): the subject header for email.
        body (string): the body of the email.

    Returns:
        MIMEMultipart Object: contains a message formated for an email message.
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg_body = body
    msg.attach(MIMEText(msg_body))
    return msg

def send_email(sender_email, sender_passsword, recipient_email, mesage_subject, message_body):
    """
    Logins into senders email and sends an email to selected recipient email.
   
    Parameters:
        sender_email (string): the senders email (from).
        sender_passsword (string): the senders login password.
        recipient_email (string): the recipient email (to).
        subject (string): the subject header of the email.
        body (string): the body of the email.

    Returns:
        Boolean: true if the email was sent successfully, false otherwise.
    """
    message = build_message(sender_email, recipient_email, mesage_subject, message_body)

    try: 
        # Connect to the smtp mailing server
        mailserver = smtplib.SMTP(SMTP_SERVER, PORT)

        # identify that this client supports ESMTP
        mailserver.ehlo() 
    
        # start tls encrypted connection, so sent email is encrypted
        mailserver.starttls()

        # identify again (required after encrypted connection is established)
        mailserver.ehlo()
        
        # login and send email
        mailserver.login(sender_email, sender_passsword)
        mailserver.sendmail(sender_email, recipient_email, message.as_string())
        mailserver.quit()
        print("Email Sent")
        return True

    except Exception as error:
        print(error)
        print("Exiting application!")
        return False
