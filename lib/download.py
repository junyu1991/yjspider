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

        #init the log ,redis
        self._log=tools.My_Log(logname=download_url,logfile='downloader')
        self._init_redis(redis_config)
        self._redis_init_key=download_url

        #The threading status,stop and pause 
        self._stop=False
        self._pause=False


        print("Download pid %d " % os.getpid())

    def _init_redis(self,redis_config):
        self._redis=redis_tool.redis_tool(config_file=redis_config)
        self._redis_enable=self._redis.get_init_status()
        self._r=self._redis.get_redis()

    def _init_redis_variable(self):
        '''
        Get the download url list name and downloaded url set
        '''
        if self._redis_enable:
            #the download list name
            self._download_list=self._r.hget(self._redis_init_key,'download_url')

            #the downloaded set name
            self._downloaded_set=self._r.hget(self._redis_init_key,'downloaded_url')

            #the file path to save the download file
            self._file_path=self._r.hget(self._redis_init_key,'download_filepath')
        else:
            pass

    def _get_download_task(self):
        '''
        Get the download url list
        @return:return the url wait to be downloaded
        '''
        if self._redis_enable:
            #temp=self._r.lrange(self._download_list,start,end)
            #return [t for t in temp if not self._r.sismember(self._downloaded_set,t)]
            while True:
                if self._r.llen(self._download_list):
                    url=self._r.lpop(self._download_list)
                    if not self._r.sismember(self._downloaded_set):
                        return url
                else:
                    time.sleep(10)
        else:
            return None

    def _add_downloaded(self,downloaded_url):
        '''
        Add the downloaded url to the redis
        @param downloaded_url:the url to add to the redis
        '''
        if self._redis_enable:
            self._r.sadd(self._downloaded_set,downloaded_url)
        else:
            pass

    def stop(self):
        '''
        Stop the threading
        '''
        self._stop=True

    def paused(self):
        '''
        Pause the threading
        '''
        self._pause=True

    def resume(self):
        '''
        Resume the threading
        '''
        self._pause=False

    def get_pause_status(self):
        return self._pause

    def run(self):
        if self._redis_enable:
            while True:
                if self._stop:
                    print("Existing the download threading")
                    break
                if not self._pause:
                    url=self._get_download_task()
                    self._download(url=url)
                else:
                    continue

    def download(self,url='http://zt.bdinfo.net/speedtest/wo3G.rar',filepath=self._file_path):
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
            self._add_downloaded(url)
        except requests.ConnectTimeout,e:
            print("Download %s timeout,this will redownload later.\n%s" % (url,str(e)))
            if self._redis_enable:
                self._r.lpush(self._download_list,url)
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
