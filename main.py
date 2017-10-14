#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:26
# Email='wangxk1991@gamil.com'
# Desc: 系统入口文件

from src.Config import Config
from src.GitLocalHelper import GitLocalHelper
import os
from src.Core import *
from src.Log import Log


class Start():
    config = None
    conf = {}

    # 初始化系统
    @classmethod
    def init(self):
        # 加载配置
        self.config = Config()
        self.conf = self.config.get()
        # 加载日志模块
        log = Log()
        # 创建缓存文件夹
        try:
            os.makedirs(self.conf['system']['default_cache'])
        except OSError:
            pass
        if not os.path.isdir(self.conf['system']['default_cache']):
            print('FATAL: Output path is not a directory or does not exist')
            sys.exit(1)

    # 执行函数
    @classmethod
    def run(self):
        sources = self.config.get('system.code_source')
        for source in sources:

            if source['enable'] is True:
                if source['type'] == 'git-local':
                    rundir = os.getcwd()
                    helper = GitLocalHelper()
                    for io in source['io']:
                        cachefile = os.path.join(self.conf['system']['default_cache'], md5(io['input']))
                        os.chdir(io['input'])
                        helper.loadCache(cachefile)
                        helper.collect(io['input'], conf=self.conf['git'])
                        helper.saveCache(cachefile=cachefile)
                        helper.refine()
                        os.chdir(rundir)
                        print(helper.authors)
            pass

    # 入口函数
    @classmethod
    def start(self):
        self.init()
        self.run()


if __name__ == '__main__':
    Start.start()
    pass
