#!/usr/bin/env python
#!encoding:utf-8

from bs4 import BeautifulSoup
import redis_tool
import tools
import urlparse
import re

import codes

class Resp_Handler():
    '''
    The reponse handler,handle the response
    '''

    def __init__(self,handler_name="",redis=None):
        '''
        @param handler_name:the reponse hanle name,used as the key of the redis
        @param redis_config:the redis config file
        '''
        self.name=handler_name
        self._init_log(log_name=self.name,log_file='resp-handler')
        self._redis_enable=True if redis else False
        self._r=redis
        #self._init_redis(redis_config)

    def set_redis(self,redis=None):
        if redis:
            self._r=redis
            self._redis_enable=True
        else:
            self._redis_enable=False


    def _init_redis(self,redis_config):
        '''
        初始化Redis(Init the redis)
        @param redis_config:the redis client config file which include redis server ip,port,password and db etc
        '''
        self._log.debug('Init redis')
        self._redis=redis_tool.redis_tool(redis_config)
        self._redis_enable=self._redis.get_init_status()
        if self._redis_enable:
            self._r=self._redis.get_redis()
            self._log.debug("Init redis success")
        else:
            self._log.warning('Init redis failed')

    def _init_log(self,log_name,log_file):
        '''
        Init the log tool
        @param log_name:the logger name
        @param log_file:the log file
        '''
        self._log=tools.My_Log(logname=log_name,logfile=log_file)


    def _get_soup(self,data):
        '''
        data=data.decode('utf-8').encode('utf-8')
        with open('text.txt','wb') as f:
            f.write(data)
        '''
        self._soup=BeautifulSoup(data,'lxml')
        #print(self._soup.find_all('img'))

    def _handle_header(self,resp):
        '''
        Handle response header,get content-type,content-length,status code
        @param resp:requests response object
        '''
        header=resp.headers
        content_type=header.get('content-type')
        content_length=header.get('conent-length')
        if resp.status_code==200:
            if content_length and int(content_length) > codes.content_length:
                self.handle_big_file(resp)
                return
            #self._get_soup(resp.content)
            if content_type and re.search('(html|xml)',content_type):
                self._get_soup(resp.content)
                self.handle_html()
            elif content_type and re.search('(javascript|css)',content_type):
                self.handle_static_files(url=resp.url)
            elif content_type and re.search('image',content_type):
                self.handle_img(url=resp.url)
            else:
                self.handle_other(url=resp.url)


    def handle_big_file(self,resp):
        '''
        Handle the resp which content-length is bigger than the codes.py.content_length
        @param resp:the response object
        '''
        pass

    def handle_data(self,response):
        print("Parsing %s " % response.url)
        self._handle_header(response)
        response.close()
        url=response.url
        '''
        self.handle_link()
        self.handle_img()
        self.handle_static_files()
        self.handle_html()
        '''

        #Update parsed url database
        #parsed='parsed_'+self.name
        if self._redis_enable:
            parsed=self._r.hget(self.name,codes.parsed_set)
            self._r.sadd(parsed,url)
        return None

    def handle_other(self,url):
        '''
        Handle other response like audio,video
        @param url:the response url
        '''
        pass


    def handle_link(self):
        a_link=[a.get('href') for a in self._soup.find_all('a') if a.get('href')]
        if not self._redis_enable:
            return
        self._log.debug("putting url into redis %s " % self.name)
        for a_l in a_link:
            #pass
            self._r.lpush(self._r.hget(self.name,codes.url),urlparse.urldefrag(a_l)[0])

    def handle_img(self,url):
        '''
        Handle img link from reponse or url
        @param url:if url is not None,just put the url to the download list
        '''
        if not self._redis_enable:
            return
        download_url=self._r.hget(self.name,codes.download_url)
        if url:
            self._r.lpush(download_url,url)
            return

        img_link=[img.get('src') for img in self._soup.find_all('img') if img.get('src')]
        self._log.debug('putting download url to %s ' % download_url)
        print ("putting to %s " % download_url)
        for i_l in img_link:
            #print(i_l)
            self._r.lpush(download_url,i_l)

    def handle_static_files(self,url):
        js=[sc.get('src') for sc in self._soup.find_all('script') if sc.get('src')]
        css=[cs.get('href') for cs in self._soup.find_all('link') if cs.get('href')]


    def handle_html(self):
        '''
        Handle reponse content html,xml
        '''
        self.handle_link()
        self.handle_img(url=None)
        self.handle_static_files(url=None)
