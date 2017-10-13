#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 下午9:46
# Email="wangxk1991@gamil.com"
# Desc : 核心功能
import time
import sys
import subprocess
import platform
import os

ON_LINUX = (platform.system() == 'Linux')


def getpipeoutput(cmds, quiet=False):
    global exectime_external
    start = time.time()
    if not quiet and ON_LINUX and os.isatty(1):
        print('>> ' + ' | '.join(cmds), sys.stdout.flush())
    p = subprocess.Popen(cmds[0], stdout=subprocess.PIPE, shell=True)
    processes = [p]
    for x in cmds[1:]:
        p = subprocess.Popen(x, stdin=p.stdout, stdout=subprocess.PIPE, shell=True)
        processes.append(p)
    output = p.communicate()[0]
    for p in processes:
        p.wait()
    end = time.time()
    if not quiet:
        if ON_LINUX and os.isatty(1):
            print('\n[%.5f] >> %s' % (end - start, ' | '.join(cmds)))
    exectime_external += (end - start)
    return output.rstrip('\n')
