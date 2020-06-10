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
def txt2string(path, code):
    """
    Turns text file to string
    :param path: The file path to text file
    :param code:  The type of encoding
    """
    with open(path, encoding = code) as f:
        result = f.read()
    return result

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

def jtbmain():
    subject = "REJECT TERROR BILL"
    content = (random.choice(txt2list(os.path.join(BASEDIR, 'jtbcontent.txt'), "utf8")))
    sender = USER
    receiver = (random.choice(txt2list(os.path.join(BASEDIR, 'jtbemails.txt'), "utf8")))
    sendmail(sender, receiver, subject, content)

def blmmain(place):
    subject = "BLACK LIVES MATTER"
    content = (f"Hello, I am concerned citizen based in {place} talking to you today to urge you to defund the police." + (txt2string(os.path.join(BASEDIR, 'blmletter.txt'), "utf8")))
    sender = USER
    receiver = (random.choice(txt2list(os.path.join(BASEDIR, 'blmemails.txt'), "utf8")))
    sendmail(sender, receiver, subject, content)

def main():
    print(""" This python script can send multiple emails to your representatives about modern issues.
    The emails to defund police is for CA, you can cater any of the .txt files to fit your agenda.
    ***The .env file contains a template for your email and password.***
    """)
    issuechoice = input("Are you emailing about BLM or TERROR BILL? ")
    if issuechoice.upper() == "BLM":
        place = input("Where are you based in? (Format: City, CA")
        blmcount = input("How many emails?")
        current_count = 0
        while current_count < int(blmcount):
            blmmain(place)
            current_count += 1
            time.sleep(.10)
        print("Done. You sent " + str(blmcount) +"emails.")
    elif issuechoice.upper() == "TERROR BILL":
        jtbcount = input("How many emails?")
        current_count = 0
        while current_count < int(jtbcount):
            jtbmain()
            current_count += 1
            time.sleep(.10)
        print("Done. You sent " + str(jtbcount) + "emails.")
    else:
        print("That was not a valid answer. Try again.")
        main()

smtp_init()
main()

#@tl.job(interval=timedelta(seconds=180))
#def mailevery3():
