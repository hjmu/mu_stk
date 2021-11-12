#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sys
from environs import Env
from loguru import logger
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
# from Utils import Utils
import traceback
# from CONST import  *
from BASE import BASE

class Mailer(BASE):
    def __init__(self):
        BASE.__init__(self)



    def send(self):

        mail_host = "smtp.gmail.com"
        mail_user = "njxhl2013@gmail.com"
        mail_pass = "mymuhj123!"

        sender = 'njxhl2013@gmail.com'
        receivers = ['hjmu2007@gmail.com']

        message = MIMEMultipart()

        # message = MIMEText('Python test...', 'plain', 'utf-8')
        message['From'] = Header("mu", 'utf-8')
        message['To'] = Header("hj", 'utf-8')
        message['Subject'] = Header('Python SMTP test', 'utf-8')

        # 正文内容
        message.attach(MIMEText('mail test……', 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的文件
        att1 = MIMEText(open(self.FRONT_LOG_FILE, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="mylog.txt"'
        message.attach(att1)

        flag_mail_ssl = 0
        try:
            smtpObj = None
            if flag_mail_ssl:
                smtpObj = smtplib.SMTP_SSL()
            else:
                smtpObj = smtplib.SMTP(mail_host)

            # smtp = smtplib.SMTP('smtp.gmail.com')
            # smtp.connect('smtp.gmail.com','587')

            #   smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 587)

            smtpObj.ehlo()  # 向Gamil发送SMTP 'ehlo' 命令
            smtpObj.starttls()

            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())

            smtpObj.quit()

            logger.info("Mail OK")
        except Exception as e:
            # print(e)
            logger.info(traceback.format_exc())
        # except smtplib.SMTPException:
        #    print("Error: 无法发送邮件")

if __name__ == "__main__":
    Mailer().send()