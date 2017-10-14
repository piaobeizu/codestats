#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/14 下午1:14
# Email="wangxk1991@gamil.com"
# Desc: 日志打印
import logging
from src.Config import Config


class Log():
    def __init__(self):
        if Config.get("system.debug") == True:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                                datefmt='%a, %d %b %Y %H:%M:%S',
                                filename='myapp.log',
                                filemode='w')

    pass


if __name__ == '__main__':
    pass
