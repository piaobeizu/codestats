#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 17-10-15 上午12:20
# Email="wangxk1991@gamil.com"
# Desc: 通知基类
class Notify():
    def __init__(self):
        pass

    # 创建通知内容
    def create(self, data):
        self.data = data

    def html_linkify(self,text):
        return text.lower().replace(' ', '_')


    def html_header(self,level, text):
        name = self.html_linkify(text)
        return '\n<h%d><a href="#%s" name="%s">%s</a></h%d>\n\n' % (level, name, name, text, level)
    pass
