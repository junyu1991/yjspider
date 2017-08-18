#!/usr/bin/env python
#!encoding:utf-8

import urllib2
import os
import urlparse
import time
import threading

import tools
import redis_tool
import requests

class Download():
    '''
    A class provide download method,use multi-threading to download file.
    Get task from the method who call the add_task()
    This class is used to download some file which has small file size
    '''

    def __init__(self,redis_config,download_url):
        self._log=tools.My_Log(logname=download_url,logfile='downloader')
        self._init_redis(redis_config)
        self._redis_key='download_'+download_url
        self._root_url=download_url
        print("Download pid %d " % os.getpid())

    def _init_redis(self,redis_config):
        self._redis=redis_tool.redis_tool(config_file=redis_config)
        self._redis_enable=self._redis.get_init_status()
        self._r=self._redis.get_redis()

    def run(self):
        downloaded='downloaded_'+self._redis_key
        print downloaded
        count=0
        if self._redis_enable:
            while True:
                url_d=self._r.lpop(self._redis_key)
                url_d=urlparse.urljoin(self._root_url,url_d)
                if not self._r.sismember(downloaded,url_d):
                    self._log.debug('downloading %s ' % url_d)
                    self.download(url=url_d)
                    #self._log.debug('downloaded %s' % url_d)
                    #self._r.sadd(downloaded,url_d)
                    time.sleep(3)
                else:
                    print('downloaded url %s'%url_d)
                    count+=1
                if count==20:
                    print('sleeping..............')
                    time.sleep(3)
                    count=0

    def add_task(self,url):
        '''
        Add download task to the downloader
        @param:url,the downloda url
        '''
        self.__task.append(url)

    def download(self,url='http://zt.bdinfo.net/speedtest/wo3G.rar',filepath='./tempdown'):
        '''
        Download file from website to local file
        @param:url,download url
        @param:filepath:the file location u want to save file
        @return:None
        '''
        if not url:
            return
        print('downloading:%s' % url)
        r=requests.get(url,stream=True,timeout=5)
        filename=os.path.join(filepath,'.'+urlparse.urlsplit(url).path)
        chunk_size=1024*1024
        print filename
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        try:
            with open(filename,'wb')  as f:
                for data in r.iter_content(chunk_size=chunk_size):
                    #data=temp.read(1024*1024)
                    f.write(data)
            self._r.sadd('downloaded_'+self._redis_key,url)
        except requests.ConnectTimeout,e:
            print("Download %s timeout,this will redownload later.\n%s" % (url,str(e)))
            if self._redis_enable:
                self._r.lpush(self._redis_key,url)
        except Exception,e1:
            print('Download %s exception.\n%s' % (url,str(e1)))
'''
if __name__=='__main__':
    d=Download()
    url='https://pic1.zhimg.com/v2-cb9e7dcb1e34b50c00af5e55582ce244_b.png'
    d.download(filepath='/home/yujun/temp/')
'''

class Downloader():
    '''
    The Downloader class, get download task from redis,
    Use multiprocess to download the file,every process download a file or mutil files.
    This is a indepent process
    '''
    def __init__(self):
        pass
