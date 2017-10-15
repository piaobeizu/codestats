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
from src.Config import Config
import time


class Email(Notify):
    emailConf = {}
    message = None

    def __init__(self):
        super().__init__()
        self.emailConf = Config.get('system.email')

    def create(self, helper):
        Notify.create(self, helper)
        self.message = MIMEText(self.emailConf['mime_text'] + time.strftime("%Y-%m-%d", time.localtime()), 'html',
                                'utf-8')
        self.message['From'] = Header(self.emailConf['from'], 'utf-8')
        self.message['To'] = Header(self.emailConf['to'], 'utf-8')
        subject = self.makeSubject(helper=helper)
        self.message['Subject'] = Header(subject, 'utf-8')
        pass

    def push(self, sender=None, receivers=[]):
        if sender == None:
            sender = self.emailConf['email_sender']
        if len(receivers) == 0:
            Log.error('邮件接收方为空。', False)
        smtpObj = smtplib.SMTP_SSL(self.emailConf['default_email_server'], port=self.emailConf['port'])
        smtpObj.set_debuglevel(1)
        smtpObj.ehlo(self.emailConf['default_email_server'])
        smtpObj.login(sender, 'nzobtmadxgvwddcf')
        try:
            Log.info('开始发送邮件...')
            smtpObj.sendmail(sender, receivers, self.message.as_string())
            Log.info("邮件发送成功!!!")
        except smtplib.SMTPException as e:
            Log.error(("Error: 无法发送邮件。错误信息：%s") % e.strerror, False)
            smtpObj.close()
        finally:
            smtpObj.quit()
        pass

    # 创建邮件发送内容
    def makeSubject(self, helper):
        content = ''
        # 生成List of Authors
        content += self.html_header(2, 'List of Authors') + '<table class="authors sortable" id="authors">' + \
                   '<tr><th>Author</th><th>Commits (%)</th><th>+ lines</th><th>- lines</th><th>First commit</th><th>Last commit</th><th class="unsortable">Age</th><th>Active days</th><th># by commits</th></tr>'

        for author in helper.getAuthors(Config.get('system.git')['max_authors']):
            info = helper.getAuthorInfo(author)
            content += '<tr><td>%s</td><td>%d (%.2f%%)</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>%d</td></tr>' % (
            author, info['commits'], info['commits_frac'], info['lines_added'], info['lines_removed'],
            info['date_first'], info['date_last'], info['timedelta'], info['active_days'], info['place_by_commits'])
        return content
        pass


