#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:25
# Email="wangxk1991@gamil.com"
# Desc: 系统配置项

system = {
    # 代码源
    "CODE_SOURCE": [
        {"type": "local", "path": [], "enable": False},
        {"type": "remote", "route": [], "enable": False},
        {"type": "git", "url": [], "enable": True},
    ]
}

config = [
    # {"module": "config.settings", "key": "settings", "load": True},
    {"module": "config.test", "key": "test", "enable": True}
]
