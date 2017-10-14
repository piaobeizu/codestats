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
                    'input': '/home/steven/develop/code/pycharm/codestats',
                    'output': {
                        'web': '',  # 生成web项目的目录地址
                        'email': ['897994454@qq.com'],  # 发送email的地址
                        'sms': []  # 发送sms短信通知的电话号码
                    }
                },
                # {
                #     'input': '/Users/steven/develop/code/intellij/rootech/root-portal',
                #     'output': {
                #         'web': '',  # 生成web项目的目录地址
                #         'email': ['897994454@qq.com'],  # 发送email的地址
                #         'sms': []  # 发送sms短信通知的电话号码
                #     }
                # }
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
    'abspath':os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
}

config = [
    # {'module': 'config.settings', 'key': 'settings', 'load': True},
    {'module': 'config.git', 'key': 'git', 'enable': True}
]
