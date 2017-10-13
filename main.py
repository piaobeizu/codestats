#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:26
# Email="wangxk1991@gamil.com"
# Desc: 系统入口文件

from src.Config import Config


class Start():
    config = None
    conf = {}

    # 初始化系统
    @classmethod
    def init(self):
        # 加载配置
        self.config = Config()
        self.conf = self.config.config

    # 执行函数
    @classmethod
    def run(self):
        sources = self.config.get("system.CODE_SOURCE")
        for source in sources:
            if source['enable'] is True:
                if source['type'] is "git":
                    print(source)
            pass

    # 入口函数
    @classmethod
    def start(self):
        self.init()
        self.run()


if __name__ == '__main__':
    Start.start()
    pass
