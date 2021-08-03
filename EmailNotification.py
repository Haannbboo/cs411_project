import smtplib
from email.mime.text import MIMEText
import random

class EmailNot():
    def __init__(self):
        pass

    def send_email(self,sender,receiver,psd,subject,content):
        """
        This can only be used as sina email
        """
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        try:
            s = smtplib.SMTP_SSL('smtp.sina.cn')
            s.login(sender,psd)
            s.sendmail(sender,receiver,msg.as_string())
            print('Email Sent')
        except smtplib.SMTPException:
            print('Fail To Send')
            return content[-7:]

    def gen_ran_num(self):
        ranstr = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',6)
        ranstr = ''.join(ranstr)
        return ranstr


