# import imapclient #mail access
import os
import smtplib
import email
import random
from dotenv import load_dotenv
import time
import tkinter
from timeloop import Timeloop
from datetime import timedelta

BASEDIR = os.path.abspath(os.path.dirname(__file__))  # get path to this file dir
load_dotenv(os.path.join(BASEDIR, '.env'))  # connects to .env file
USER = os.getenv("EMAIL")
PASSWORD = os.getenv("TOKEN")
tl = Timeloop()

def sendmail(sender, receiver, subject, content):
    """
    Sends an email.
    :param sender: The address of the person sending the text
    :param receiver: The address of the person receiving the text
    :param subject: The subject of the email
    :param content: The content of the email
    """
    msg = email.message.EmailMessage()
    msg['from'] = sender
    msg["to"] = receiver
    msg["Subject"] = subject
    msg.set_content(content)
    res = s.send_message(msg)

def smtp_init():
    """
    Initialize SMTP connection
    """
    print("Initializing SMTP....")
    global s
    s = smtplib.SMTP('imap.gmail.com', 587)  # connects to GMAIL server w/ port 587 | s is global
    c = s.starttls()[0]  # starts tls, c = the returned status code
    if c != 220:
        raise Exception('Starting tls failed: ' + str(c))
    c = s.login(USER, PASSWORD)[0]
    if c != 235:
        raise Exception('SMTP login failed: ' + str(c))
    print("Done. ")
    # s.ehlo()  # identifies self to server


def txt2list(path, code):
    """
    Turns text file to a list.
    :param path: The file path to the text file
    """
    with open(path, encoding = code) as f:
        result = f.read().splitlines()
    return result

def jtbmain():
    subject = "REJECT TERROR BILL"
    content = (random.choice(txt2list(os.path.join(BASEDIR, 'jtbcontent.txt'), "utf8")))
    sender = USER
    receiver = (random.choice(txt2list(os.path.join(BASEDIR, 'jtbemails.txt'), "utf8")))
    sendmail(sender, receiver, subject, content)

smtp_init()

@tl.job(interval=timedelta(seconds=180))
def mailevery3():
    jtbmain()
    print("sent")

if __name__ == "__main__":
    tl.start(block=True)