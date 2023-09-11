from flask import Flask, jsonify,make_response

from flask_cors import CORS

import requests

from flask import request

from flask_restful import Resource, Api

from celery import Celery
from redis import Redis



import datetime



from APIs import *
# from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from jwt_utils import jwt

import os

from models import *

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, ForeignKey, delete
 
current_dir = os.path.abspath(os.path.dirname(__file__))

from config import *

app = Flask(__name__)

from flask_jwt_extended import JWTManager
app.config.from_object(Config)
jwt.init_app(app)
jwt = JWTManager(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(
  current_dir, "database.sqlite3")

from database import db
db.init_app(app)


# Import API routes from APIs.py
from APIs import api_routes

# Register API routes with app
app.register_blueprint(api_routes)


#configuring flask api
api = Api(app)
api.init_app(app)
   
CORS(app, resources={r"/*": {"origins": "*"}})

app.app_context().push()

engine = create_engine("sqlite:///./database.sqlite3")



"""Celery and redis configuration 2"""

redis = Redis(host='localhost', port=6379)
from datetime import timedelta

def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'], include=app.config['CELERY_INCLUDE'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
 
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app.config['CELERY_BACKEND'] = "redis://localhost:6379/0"
app.config['CELERY_BROKER_URL'] = "redis://localhost:6379/0"
app.config['CELERY_INCLUDE'] = [app.import_name]
# app.config['CELERY_ACCEPT_CONTENT'] = ['json']

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

app.config['CELERYBEAT_SCHEDULE'] = {
    'say-every-5-seconds': {
        'task': 'send_reminders',
        'schedule': timedelta(seconds=10)
    },
}

app.config['CELERY_TIMEZONE'] = 'UTC'
celery = make_celery(app)

# @celery.task(name='return_something')
# def return_something():
#     print ('something')
#     return 'something'


# """Celery and redis configuration"""

# redis = Redis(host='localhost', port=6379)
# # celery = Celery(app.name, broker='redis://localhost:6379/0')

# app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
# app.config['result_backend'] = 'redis://localhost:6379'

# celery = Celery(
#     "Application jobs",
#     broker=app.config['CELERY_BROKER_URL'],
#     backend=app.config['result_backend']
# )

# celery.conf.update(app.config)

# class ContextTask(celery.Task):
#     def __call__(self, *args, **kwargs):
#         with app.app_context():
#             return self.run(*args, **kwargs)

# celery.Task = ContextTask





""" Full code section for checking users with no 24 hour activity then sending daily reminder email"""

### send_reminder_email function part of the code

import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from jinja2 import Template

# Read this values from config 
# For testing and local development use a Fake SMTP like mailhog
# Check https://thejeshgn.com/2022/02/11/linked-list-fake-or-mock-smtp-servers-for-email-testing/

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = 1025
SENDER_ADDRESS = 'test@dp.com'
# EMAIL_HOST_USER = 'support@prettyprinted.com'
SENDER_PASSWORD = ""


from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)


def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    print("send_reminders level 5")

    if content == "html":
        msg.attach(MIMEText(message, "html"))
    else:
        msg.attach(MIMEText(message, "plain"))

    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        # Email attachments are sent as base64 encoded
        encoders.encode_base64(part)
        # From: https://www.ietf.org/rfc/rfc2183.txt
        # Bodyparts can be designated `attachment' to indicate that they are
        # separate from the main body of the mail message, and that their
        # display should not be automatic, but contingent upon some further
        # action of the user.
        part.add_header(
            "Content-Disposition", f"attachment; filename= {attachment_file}",
        )
        # Add the attchment to msg
        msg.attach(part)
    
    
    # Send email with the PDF attachment

    server = smtplib.SMTP('localhost', 1025)  # Replace with your SMTP server settings
    sender = 'admin@test.com'
    recipient = 'user@test.com'
    # body = 'Please find attached your profile statistics report.'
    # msg.attach(MIMEText(body, 'plain'))
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

    print("send_reminders level 6")
    

    # s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    # s.starttls()
    # print("send_reminders level 7")
    
    # s.login(SENDER_ADDRESS, SENDER_PASSWORD) 
    # print("send_reminders level 8")
    # s.send_message(msg)
    # print("send_reminders level 9")
    # s.quit()
    return True


def format_message(template_file, data={}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(data=data)
    
"""can turn this into send monthly report email function"""
# def send_welcome_message(data):
#     message = format_message("welcome-email.html", data=data)
#     # this can be a seaprate task
#     send_email(
#         to_address=data["email"],
#         subject="Welcome",
#         message=message,
#         content="html",
#         attachment_file="manual.pdf",
#     )

def send_reminder_email(user): 
    print("send_reminders level 3")
    message = "Hey {}, you have not visited our site in the last 24 hours. See what your friends are upto!".format(user.name)
    # this can be a seaprate task
    send_email(
        to_address= user.email,
        # to_address= 'ciconor573@duiter.com',
        subject="Blog Lite, See Whats Cooking",
        message=message,
        content="text",
        attachment_file=None,
    )
    print("send_reminders level 4")


### checks for users with no 24 hour activity then sends daily reminder email

from datetime import datetime, timedelta

@celery.task(name="send_reminders")
def send_reminders():
    print("send_reminders level 1")
    user_list = users.query.all() 
    for user in user_list:
        # Check if the user has not visited/posted anything in the last 24 hours
        last_activity = user.last_activity
        if last_activity is None or datetime.utcnow() - last_activity > timedelta(hours=24):
            # Send a reminder email to the user
            send_reminder_email(user)
            print("hello from send_reminders test")
    print("send_reminders level 2")

# code that scedules reminders to be sent daily at 6pm by calling send_reminders function
from celery.schedules import crontab

# celery.conf.beat_schedule = {
#     'send-reminders-daily': {
#         'task': 'send_reminders',
#         'schedule': crontab(hour=13, minute=9),
#         'args': (),
#         'options': {
#             'timezone': 'Asia/Kolkata'
#         }
#     }
# }

# celery.conf.update(
#     CELERY_TIMEZONE='Asia/Kolkata',
#     # other configuration variables here
# )

# send_reminders() # this is to test the function

""" Full code section for  generating and sending pdf report to users"""

from weasyprint import HTML
from flask import Flask, request, make_response, jsonify 
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    html = request.json['html']
    data = request.json['data']

    # Use WeasyPrint to generate a PDF from the HTML and data
    pdf = HTML(string=html.format(**data)).write_pdf()

    # Create a response with the PDF as the content
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=profile_stats.pdf'

    # Send email with the PDF attachment
    server = smtplib.SMTP('localhost', 1025)  # Replace with your SMTP server settings
    sender = 'admin@test.com'
    recipient = 'user@test.com'
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = 'Profile Statistics Report'
    body = 'Please find attached your profile statistics report.'
    msg.attach(MIMEText(body, 'plain'))
    attachment = MIMEBase('application', 'pdf')
    attachment.set_payload(response.get_data())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='profile_stats.pdf')
    msg.attach(attachment)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

    return response


if __name__ == '__main__':
    
    app.run(debug = True)
