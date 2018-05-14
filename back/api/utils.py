from flask import make_response
import sendgrid
import os
from sendgrid.helpers.mail import *
import smtplib 

JSON_MIME_TYPE = 'application/json'
email_to = 'accounts@oddeven.ch'

def search_book(books, book_id):
    for book in books:
        if book['id'] == book_id:
            return book

def json_response(data='', status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(data, status, headers)

def search_workshop(workshops, workshop_id):
    for workshop in workshops:
        if workshop['id'] == workshop_id:
            return workshop

def send_email(recipient, content):
    VCAP_SERVICES = os.environ['VCAP_SERVICES']
    credentials = VCAP_SERVICES['sendgrid'][0]['credentials']
    smtpserver = smtplib.SMTP(credentials['hostname'], 587)
    smtpserver.ehlo()
    smtpserver.login(credentials['username'], credentials['password'])
    header = 'To:' + email_to + '\n' + 'From: ' + 'Workshops <accounts@oddeven.ch>' + '\n' + 'Subject: A new workshop has been ordered!\n'
    msg = header + '\n\n ' + content + ' \n\n'
    smtpserver.sendmail(username, email_to, msg)
    smtpserver.close()
    print('Email sent successfully')
