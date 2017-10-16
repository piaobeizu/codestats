#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/13 下午9:46
# Email="wangxk1991@gamil.com"
# Desc : 核心基础功能
import time
import sys
import subprocess
import platform
import os
import hashlib
from src.Log import Log

exectime_internal = 0.0
exectime_external = 0.0
ON_LINUX = (platform.system() == 'Linux')
VERSION = 0


def getpipeoutput(cmds, quiet=False):
    global exectime_external
    start = time.time()
    if not quiet and ON_LINUX and os.isatty(1):
        Log.info('>> ' + ' | '.join(cmds), sys.stdout.flush())
    p = subprocess.Popen(cmds[0], stdout=subprocess.PIPE, shell=True)
    processes = [p]
    for x in cmds[1:]:
        p = subprocess.Popen(x, stdin=p.stdout, stdout=subprocess.PIPE, shell=True)
        processes.append(p)
    output = p.communicate()[0].decode()
    for p in processes:
        p.wait()
    end = time.time()
    if not quiet:
        if ON_LINUX and os.isatty(1):
            Log.info('[%.5f] >> %s' % (end - start, ' | '.join(cmds)))
    exectime_external += (end - start)
    return output.rstrip('\n')


def getkeyssortedbyvalues(dict):
    return list(map(lambda el: el[1], sorted(map(lambda el: (el[1], el[0]), dict.items()))))


# dict['author'] = { 'commits': 512 } - ...key(dict, 'commits')
def getkeyssortedbyvaluekey(d, key):
    return list(map(lambda el: el[1], sorted(map(lambda el: (d[el][key], el), d.keys()))))


def getversion():
    global VERSION
    if VERSION == 0:
        VERSION = getpipeoutput(["git rev-parse --short HEAD"]).split('\n')[0]
    return VERSION


def md5(encrypt):
    m2 = hashlib.md5()
    m2.update(encrypt.encode("utf-8"))  # 参数必须是byte类型，否则报Unicode-objects must be encoded before hashing错误
    return m2.hexdigest()
