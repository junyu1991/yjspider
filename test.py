#!/usr/bin/env python
#!encoding:utf-8

from yjspider import *

from lib import download

if __name__=='__main__':
    yj=yjspider(redis_config='./config/redis-config.json')
    url='http://jandan.net/ooxx'
    #yj.start(url=url)
    d=download.Download(redis_config='./config/redis-config.json',download_url=url)
    d.run()
