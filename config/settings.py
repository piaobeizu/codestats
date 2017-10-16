#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:25
# Email='wangxk1991@gamil.com'
# Desc: 系统配置项
import os

system = {
    # 代码源
    'code_source': [
        {
            'type': 'local',
            'io': [
                {
                    'input': '',
                    'output': {}
                }
            ],
            'enable': False
        },
        {
            'type': 'remote',
            'io': [
                {
                    'input': '',
                    'output': {}
                }
            ],
            'enable': False
        },
        # 在git本地仓库下统计
        {
            'type': 'git-local',
            'io': [
                {
                    'input': '',
                    'output': {
                        'web': '',  # 生成web项目的目录地址
                        'email': [],  # 发送email的地址
                        'sms': []  # 发送sms短信通知的电话号码
                    }
                }
            ],
            'enable': True
        },
        # 统计git远程仓库
        {
            'type': 'git-remote',
            'io': [
                {
                    'input': '',
                    'output': {}
                }
            ],
            'enable': False
        },
    ],
    'default_cache': '/tmp/codestat',
    'abspath': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'git': {
        'max_domains': 10,
        'max_ext_length': 10,
        'style': 'gitstats.css',
        'max_authors': 20,
        'default_branch': 'dev'
    },
    'email': {
        'email_sender': '',
        'default_email_server': 'smtp.163.com',
        'port': 25,
        'from': '',
        'to': u'',
        'receiver_cc': [],
        'subject': ''
    },
}

config = [
    # {'module': 'config.settings', 'key': 'settings', 'load': True},
    {'module': 'config.git', 'key': 'git', 'enable': True}
]
