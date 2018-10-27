#!/usr/bin/env python
"""
this class handles sending emails
"""
__author__ = "Michael Montuori [michael.montuori@gmail.com]"
__copyright__ = "Copyright 2017 Michael Montuori. All rights reserved."
__credits__ = ["Warren Crigger"]
__license__ = "GPLv3"
__version__ = "0.1"
__revision__ = "1"

import logging
import smtplib
from email.mime.text import MIMEText

class EMail(object):

    def __init__(self):
        logging.debug('instantiating EMail class...')
        self.__mail_from = None
        self.__mail_to = None
        self.__subject = None
        self.__message = None
        self.__smtp_server = None
        self.__smtp_port = None
        self.__smtp_user = None
        self.__smtp_password = None

    def set_from(self, mail_from):
        self.__mail_from = mail_from

    def set_to(self, mail_to):
        self.__mail_to = mail_to

    def set_subject(self, subject):
        self.__subject = subject

    def set_message(self, message):
        self.__message = message

    def set_smtp_server(self, smtp_server):
        self.__smtp_server = smtp_server

    def set_smtp_port(self, smtp_port):
        self.__smtp_port = smtp_port

    def set_smtp_user(self, smtp_user):
        self.__smtp_user = smtp_user

    def set_smtp_password(self, smtp_password):
        self.__smtp_password = smtp_password

    def send(self):
        logging.info('sending email message to: ' + self.__mail_to)
        logging.info('email subject: ' + self.__subject)
        if self.__mail_to is None:
            raise Exception('EMail to must not be None')
        if self.__subject is None:
            raise Exception('EMail subject must not be None')
        if self.__message is None:
            raise Exception('EMail message must not be None')
        if self.__smtp_server is None:
            raise Exception('EMail smtp server must not be None')
        msg = MIMEText(self.__message)
        msg['Subject'] = self.__subject
        msg['From'] = self.__mail_from
        msg['To'] = self.__mail_to
        s = smtplib.SMTP(self.__smtp_server, self.__smtp_port)
        #s.connect(self.__smtp_server, "submission")
        s.ehlo()
        s.starttls()
        s.ehlo()
        if self.__smtp_user is not None:
            s.login(self.__smtp_user, self.__smtp_password)
        s.sendmail(self.__mail_from, self.__mail_to, msg.as_string())
        s.quit()