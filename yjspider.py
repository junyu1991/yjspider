#!/usr/bin/env python
#!encoding:utf-8

import redis

from lib import redis_tool

#the manage key to manage the spider
manage_key='yjspider'

class yjspider():

    def __init__(self,redis_config,url=''):
        '''
        Init the redis,crawler,downloader
        @param redis_config:the redis config file
        @param url:the spider start url
        '''
        self._init_redis(redis_config)
        self._init_log()
        self._url=url

    def _init_redis(self,redis_config):
        '''
        Init the redis connection
        @param redis_config:the redis config file
        '''
        temp_redis=redis_tool.redis_tool(redis_config)
        self._redis_enable=temp_redis.get_init_status()
        self._redis=temp_redis.get_redis()

    def _init_log(self):
        pass


    def start(self,url=self._url):
        '''
        Start the spider
        '''

        #handle the redis
        self._handle_redis(url)

        #start crawler



        #start downloader


    def _handle_redis(self,url):
        '''
        Create hash in the redis based on url,the hash include key :url,the url list(name) wait to crawl;
        parsed_url,the parsed url;download_url the url wait to be downloaded;downloaded_url, the downloaded url;
        download_path,the file location to save the file.
        The hash key is url
        '''
        if self._redis_enable:
            #put the url to the all set
            self._r.sadd(manage_key,url)

            #create spider hash
            url_name=get_md5(url)
            parsed_set=get_md5('parsed_'+url)
            download_name=get_md5('download_'+url)
            downloaded_set=get_md5('downloaded_'+url)
            download_path='./tempdown'
            hash_dict={'url':url_name,'parsed_url':parsed_set,'download_url':download_name,'downloaded_url':downloaded_set,'download_path':download_path}
            self._r.hmset(url,hash_dict)
        else:
            print('The redis not enable')


def get_md5(string):
    '''
    Get the string md5
    '''
    import md5
    m=md5()
    m.update(string)
    return m.hexdigest()



