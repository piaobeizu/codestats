#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:26
# Email='wangxk1991@gamil.com'
# Desc: 系统入口文件

from src.Core import *

from src.Config import Config
from src.Log import Log
from src.helper.GitLocalHelper import GitLocalHelper


class Start():
    conf = {}
    # 初始化系统
    @classmethod
    def init(self):
        # 加载全局变量模块
        # 加载配置模块
        Config.init()
        self.conf = Config.get()
        # 创建缓存文件夹和日志文件夹
        try:
            os.makedirs(self.conf['system']['default_cache'])
            os.makedirs("/home/steven/develop/code/pycharm/codestats/log/")
        except OSError:
            pass
        if not os.path.isdir(self.conf['system']['default_cache']):
            Log.error('FATAL: Output path is not a directory or does not exist')
            sys.exit(1)

    # 执行函数
    @classmethod
    def run(self):
        sources = Config.get('system.code_source')
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
        Log.info('系统初始化。。。')
        self.init()
        Log.info('系统开始执行。。。')
        self.run()
        Log.info('执行完成。。。',True)

if __name__ == '__main__':
    Start.start()
    pass
