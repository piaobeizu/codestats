#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by wxk on 2017/10/14 下午1:14
# Email="wangxk1991@gamil.com"
# Desc: 日志打印
import logging
import sys
import os
import traceback
import io
import threading

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}
_nameToLevel = {
    'CRITICAL': CRITICAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}
if threading:
    _lock = threading.RLock()
else: #pragma: no cover
    _lock = None
if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else: #pragma: no cover
    def currentframe():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back
def _acquireLock():
    """
    Acquire the module-level lock for serializing access to shared data.

    This should be released with _releaseLock().
    """
    if _lock:
        _lock.acquire()

def _releaseLock():
    """
    Release the module-level lock acquired by calling _acquireLock().
    """
    if _lock:
        _lock.release()
def addLevelName(level, levelName):
    """
    Associate 'levelName' with 'level'.

    This is used when converting levels to text during message formatting.
    """
    _acquireLock()
    try:    #unlikely to cause an exception, but you never know...
        _levelToName[level] = levelName
        _nameToLevel[levelName] = level
    finally:
        _releaseLock()
_srcfile = os.path.normcase(addLevelName.__code__.co_filename)

class Log():
    DEBUG = True
    log=None
    @classmethod
    def init(self):
        self.log = logging
        if Log.DEBUG == True:
            self.log.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                filename='./log/codestats.log',
                                filemode='a+')
        else:
            self.log.basicConfig(format='%(asctime)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                filename='./log/codestats.log',
                                filemode='a+')
    @classmethod
    def debug(self,text,linefeed=False):
        Log.init()
        try:
            fn, lno, func, sinfo = Log.findCaller()
        except ValueError: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        self.log.debug(Log.makeText(fn,lno,'DEBUG',text,linefeed))

    @classmethod
    def info(self,text,linefeed=False):
        Log.init()
        try:
            fn, lno, func, sinfo = Log.findCaller()
        except ValueError: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        self.log.info(Log.makeText(fn,lno,'INFO',text,linefeed))

    @classmethod
    def warning(self,text,linefeed=False):
        Log.init()
        try:
            fn, lno, func, sinfo = Log.findCaller()
        except ValueError: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        self.log.warning(Log.makeText(fn,lno,'WARNING',text,linefeed))

    @classmethod
    def error(self,text,linefeed=False):
        Log.init()
        try:
            fn, lno, func, sinfo = Log.findCaller()
        except ValueError: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        self.log.error(Log.makeText(fn,lno,'ERROR',text,linefeed))

    @classmethod
    def findCaller(self, stack_info=False):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    @classmethod
    def makeText(cls,fn, lno,level,text,linefeed=False):
        file=str(fn).replace(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/",'')
        if linefeed == False:
            return '%(filename)s [line:%(lineno)d] %(levelname)s %(msg)s'%{'filename':file,'lineno':lno,'levelname':level,'msg':text}
        else:
            return '%(filename)s [line:%(lineno)d] %(levelname)s %(msg)s\n'%{'filename':file,'lineno':lno,'levelname':level,'msg':text}