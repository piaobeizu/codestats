#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 17-10-15 上午12:21
# Email="wangxk1991@gamil.com"
# Desc: 邮件发送类
import smtplib
from src.Notify import Notify
from email.mime.text import MIMEText
from email.header import Header
from src.Log import Log


class Email(Notify):
    message = None
    sender = '897994454@qq.com'

    def __init__(self):
        super().__init__()

    def create(self, data):
        Notify.create(self, data)
        self.message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
        self.message['From'] = Header("菜鸟教程", 'utf-8')
        self.message['To'] = Header("测试", 'utf-8')
        subject = 'Python SMTP 邮件测试'
        self.message['Subject'] = Header(subject, 'utf-8')
        pass

    def push(self, sender=None, receivers=[]):
        if sender == None:
            sender = self.sender
        if len(receivers) == 0:
            Log.error('邮件接收方为空。', False)
        smtpObj = smtplib.SMTP('smtp.qq.com',port=465)
        smtpObj.login('897994454@qq.com','1259381991kxqy')
        try:
            smtpObj.sendmail(sender, receivers, self.message.as_string())
            Log.info("邮件发送成功")
        except smtplib.SMTPException as e:
            Log.error(("Error: 无法发送邮件。错误信息：%s")%e.strerror, False)
            smtpObj.close()
        finally:
            smtpObj.close()
        pass
