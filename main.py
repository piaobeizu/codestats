#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 上午10:26
# Email='wangxk1991@gamil.com'
# Desc: 系统入口文件

from src.Core import *

from src.Config import Config
from src.Log import Log
from src.helper.GitLocalHelper import GitLocalHelper
from src.notify.Email import Email


class Start():
    conf = {}

    # 初始化系统
    @classmethod
    def init(self):
        # 加载全局变量模块
        # 加载配置模块
        Config.init()
        self.conf = Config.get('system')
        # 创建缓存文件夹和日志文件夹
        try:
            os.makedirs(self.conf['default_cache'])
            os.makedirs("./log/")
        except OSError:
            pass
        if not os.path.isdir(self.conf['default_cache']):
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
                        Log.info('创建缓存文件。。。')
                        cachefile = os.path.join(self.conf['default_cache'], md5(io['input']))
                        os.chdir(io['input'])
                        helper.loadCache(cachefile)
                        Log.info('开始统计。。。')
                        helper.collect(io['input'], conf=self.conf['git'])
                        helper.saveCache(cachefile=cachefile)
                        Log.info('提炼统计结果。。。')
                        helper.refine()
                        os.chdir(rundir)
                        if 'web' in io['output'].keys() and io['output']['web'].strip() != '':
                            pass
                        if 'email' in io['output'].keys() and len(io['output']['email']) != 0:
                            email  = Email()
                            email.create(helper)
                            email.push(self.conf['email']['email_sender'],io['output']['email'])
                            pass
                        if 'sms' in io['output'].keys() and len(io['output']['sms']) != 0:
                            pass
            pass

    # 入口函数
    @classmethod
    def start(self):
        Log.info('系统初始化。。。')
        self.init()
        Log.info('系统开始执行。。。')
        self.run()
        Log.info('执行完成。。。', True)


if __name__ == '__main__':
    Start.start()
    pass
