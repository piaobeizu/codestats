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
import src.Core as Core
import time


class Email(Notify):
    emailConf = {}
    message = None

    def __init__(self):
        super().__init__()
        self.emailConf = Config.get('system.email')

    def create(self, helper):
        Notify.create(self, helper)
        self.message = MIMEText(self.makeMimeText(helper), 'html', 'utf-8')
        self.message['From'] = self.emailConf['from']  # 163邮箱，此处不能用header函数，下面的to也是一样
        self.message['To'] = self.emailConf['to']
        subject = self.emailConf['subject'] + '[' + time.strftime("%Y/%m/%d", time.localtime()) + ']'
        self.message['Subject'] = Header(subject, 'utf-8')
        self.message['Cc'] = ";".join(self.emailConf['receiver_cc'])
        pass

    def push(self, sender=None, receivers=[]):
        if sender == None:
            sender = self.emailConf['email_sender']
        if len(receivers) == 0:
            Log.error('receivers of email is empty...', False)
        # smtpObj = smtplib.SMTP_SSL(self.emailConf['default_email_server'], port=self.emailConf['port'])
        # smtpObj.set_debuglevel(1)
        # smtpObj.ehlo(self.emailConf['default_email_server'])
        # smtpObj.login(sender, '')
        smtpObj = smtplib.SMTP(self.emailConf['default_email_server'], port=self.emailConf['port'])
        smtpObj.set_debuglevel(1)
        smtpObj.login(sender, '')
        try:
            Log.info('start send email...')
            smtpObj.sendmail(sender, receivers, self.message.as_string())
            # smtpObj.sendmail(sender, ";".join(receivers), self.message.as_string())
            Log.info("email send success...")
        except smtplib.SMTPException as e:
            Log.error(("Error: email send failed, error info is : %s") % e, False)
        finally:
            smtpObj.quit()
        pass

    # 创建邮件发送内容
    def makeMimeText(self, helper):
        content = '<style>table,table tr th, table tr td { border:1px solid #0094ff; }table { width: 90%; min-height: 25px; line-height: 25px; text-align: center; border-collapse: collapse;}</style>'
        # 生成author of day
        content += self.html_header(2, 'Author of day') + '<table style="border:1px solid #F00;">' + \
                   '<tr><th>Author</th><th>Add</th><th>Delete</th><th>Commits</th></tr>'
        for author in helper.getAuthors(Config.get('system.git')['max_authors']):
            info = helper.author_of_day[author]
            content += '<tr><td>%s</td><td>%d</td><td>%d</td><td>%d</td></tr>' % (
            author, info['lines_added'], info['lines_removed'], info['commit'])
        content += "</table>"
        # 生成author of month
        content += self.html_header(2, 'Author of Month') + '<table style="border:1px solid #F00;">' + \
                   '<tr><th>Month</th><th>Author</th><th>Commits (%)</th><th class="unsortable">Next top 5</th></tr>'
        for yymm in reversed(sorted(helper.author_of_month.keys())):
            authordict = helper.author_of_month[yymm]
            authors = Core.getkeyssortedbyvalues(authordict)
            authors.reverse()
            commits = helper.author_of_month[yymm][authors[0]]
            next = ', '.join(authors[1:5])
            content += '<tr><td>%s</td><td>%s</td><td>%d (%.2f%% of %d)</td><td>%s</td></tr>' % (
                yymm, authors[0], commits, (100.0 * commits) / helper.commits_by_month[yymm],
                helper.commits_by_month[yymm],
                next)
        content += "</table>"

        return content

    pass
