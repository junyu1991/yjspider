#!/usr/bin/env python
#!encoding:utf-8

import urllib2
import os
import urlparse
import time

class Download():
    '''
    A class provide download method,use multi-threading to download file.
    Get task from the method who call the add_task()
    This class is used to download some file which has small file size
    '''

    def __init__(self,task=[]):
        self.__task=task

    def add_task(self,url):
        '''
        Add download task to the downloader
        @param:url,the downloda url
        '''
        self.__task.append(url)

    def download(self,url='http://zt.bdinfo.net/speedtest/wo3G.rar',filepath='./'):
        '''
        Download file from website to local file
        @param:url,download url
        @param:filepath:the file location u want to save file
        @return:None
        '''
        temp=urllib2.urlopen(url)
        filename=os.path.join(filepath,'.'+urlparse.urlsplit(url).path)
        headers=temp.headers
        content_length=0
        if headers.has_key('content-length'):
            content_length=float(headers.get('content-length'))
            print("The %s is %s M" % (filename,str(int(content_length)/(1024*1024))))
        print filename
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename,'wb')  as f:
            data=temp.read(1024*1024)
            download_length=float(len(data))
            while ''!=data:
                begin=time.time()
                f.write(data)
                data=temp.read(1024*1024)
                end=time.time()
                download_length+=len(data)
                if end>begin and content_length!=0:
                    print("The download speed= %6.3f kb/s,%5.2f%% downloaded" % (1024/(end-begin),download_length/content_length*100))
                else:
                    print("download finish")

if __name__=='__main__':
    d=Download()
    url='https://pic1.zhimg.com/v2-cb9e7dcb1e34b50c00af5e55582ce244_b.png'
    d.download(filepath='/home/yujun/temp/')


class Downloader():
    '''
    The Downloader class, get download task from redis,
    Use multiprocess to download the file,every process download a file or mutil files.
    This is a indepent process
    '''
    def __init__(self):
        pass
