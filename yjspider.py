#!/usr/bin/env python
#!encoding:utf-8

import md5

#import redis

from lib import redis_tool
from lib import crawler
from lib import handler
from lib import codes
from lib import download

#the manage key to manage the spider
manage_key='yjspider'

class yjspider():

    def __init__(self,redis_config=None,url='',crawler=None,resp_handler=None):
        '''
        Init the redis,crawler,downloader
        @param redis_config:the redis config file
        @param url:the spider start url
        '''
        self._init_redis(redis_config)
        self._init_log()
        self._url=url

        self._crawler=crawler
        self._resp_handler=resp_handler

        #the crawler threading pool size
        self._thread_pool_size=1

    def _init_redis(self,redis_config):
        '''
        Init the redis connection
        @param redis_config:the redis config file
        '''
        temp_redis=redis_tool.redis_tool(redis_config)
        self._redis_enable=temp_redis.get_init_status()
        self._r=temp_redis.get_redis()

        print self._redis_enable
        print self._r

    def _init_log(self):
        pass

    def set_threading_pool_size(self,pool_size):
        '''
        Set crawler threding pool size
        '''
        self._thread_pool_size=pool_size

    def get_threading_pool_size(self):
        return self._thread_pool_size

    def set_crawler(self,crawler):
        '''
        Set the spider's crawler
        '''
        self._crawler=crawler

    def set_resp_handler(self,resp_handler):
        '''
        Set the crawler's response handler
        '''
        resp_handler.set_redis(self._r)
        #resp_handler.name=self._url
        self._resp_handler=resp_handler


    def start(self,url='',start_download=True):
        '''
        Start the spider
        '''

        if not url:
            print('Url empty ')
            sys.exit(0)

        #handle the redis
        self._handle_redis(url)

        if not self._resp_handler:
            self._resp_handler=handler.Resp_Handler(handler_name=url,redis=self._r)

        self._resp_handler.name=url

        #start crawler
        if not self._crawler:
            self._crawler=crawler.crawler(redis=self._r,start_url=url)
            self._crawler.set_resp_handler(self._resp_handler)
            #self._crawler.run()

        self._download=download.Download(download_url=url)
        self._crawler.start()
        self._download.start()




        #start downloader


    def _handle_redis(self,url):
        '''
        Create hash in the redis based on url,the hash include key :url,the url list(name) wait to crawl;
        parsed_url,the parsed url;download_url the url wait to be downloaded;downloaded_url, the downloaded url;
        download_path,the file location to save the file.
        The hash key is url
        '''
        print("Set manage key and hash to the redis")
        if self._redis_enable:
            #put the url to the all set
            self._r.sadd(manage_key,url)

            #create spider hash
            url_name=get_md5(url)
            parsed_set=get_md5('parsed_'+url)
            download_name=get_md5('download_'+url)
            downloaded_set=get_md5('downloaded_'+url)
            download_path='./tempdown'
            hash_dict={codes.url:url_name,codes.parsed_set:parsed_set,codes.download_url:download_name,codes.downloaded_set:downloaded_set,codes.download_filepath:download_path}
            self._r.hmset(url,hash_dict)
        else:
            print('The redis not enable')


def get_md5(string):
    '''
    Get the string md5
    '''
    m=md5.md5()
    m.update(string)
    return m.hexdigest()



