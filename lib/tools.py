#!/usr/bin/env python
#!encoding:utf-8
#date:2017-05-08

import os
import time
import traceback
import logging,logging.handlers

class My_Log():
    '''
    The logging wrapper class
    @param:logname
    @param:logfile the file you want to write the log
    '''

    import logging,logging.handlers

    def __init__(self,logname,logfile,*args):
        pre=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../log/')
        logfilename=os.path.join(pre,logfile)

        self.__logger=logging.getLogger(logname)

        filehandler=logging.handlers.TimedRotatingFileHandler(logfilename,when='midnight',encoding='utf8')
        filehandler.suffix='%Y-%m-%d.log'
        filehandler.setLevel(logging.DEBUG)

        fmt_str='%(asctime)s-[%(levelname)s]-%(name)s:%(message)s'
        formatter=logging.Formatter(fmt_str)

        filehandler.setFormatter(formatter)

        self.__logger.addHandler(filehandler)
        self.debug('Init logging tool success')

    def warning(self,message):
        self.__logger.warning(message)

    def debug(self,message):
        self.__logger.debug(message)

    def info(self,message):
        self.__logger.info(message)

    def error(self,message):
        self.__logger.error(message)

    def critical(self,message):
        self.__logger.critical(message)


def save_file():
    pass

