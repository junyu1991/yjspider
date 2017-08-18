#!/usr/bin/env python
#!encoding:utf-8

import urllib2
import re
import threading
import time
import urlparse

from bs4 import BeautifulSoup
import requests
from headers import header
import redis_tool
from handler import Resp_Handler
import tools

class crawler(threading.Thread):
    '''
    The crawler class,used to requests ,get url from redis,call resp_handler to handle _get_response
    @param redis_config:the redis config file
    @param start_url:the root url of a spider
    '''

    def __init__(self,redis_config,start_url):
        threading.Thread.__init__(self)

        #Init the requests session
        self._header=header()
        self._s=requests.Session()
        #self._s.headers.update(self._header.get_default_header())
        self._handler=Resp_Handler(start_url,redis_config)

        #Init the redis
        self._r=redis_tool.redis_tool(redis_config)
        self._redis_enable=self._r.get_init_status()

        self._start=start_url

        #Init the log tool
        self._log=tools.My_Log(logname=self._start,logfile='crawler')

    def _get_response(self,url,method='get',headers={},files=[],data=None,cookies=None,cert=None,timeout=30,**kwargs):
        method=method.upper()
        #self._s.headers.update(headers)
        pre=requests.Request(method=method,url=url,data=data,files=files)
        prepped=self._s.prepare_request(pre)
        try:
            with self._s.send(prepped,stream=True,cert=cert,timeout=timeout) as resp:
                self._header.parse_header(dict(resp.headers))
                self._s.headers.update(self._header.get_default_header())
                content_type=resp.headers.get('content-type')
                encoding=self._get_content_encoding(content_type)
                regx=re.compile('.*(text\/html|text\/xml).*')
                if resp.status_code==requests.codes.OK:
                    #Don't handle redirect url for now
                    '''
                    with open('temp.txt','wb') as f:
                        f.write(resp.content)
                    '''
                    self._handler.handle_data(resp)
                elif resp.status_code!=requests.codes.OK:
                    print("Connected url %s \t %d" % (url,resp.status_code))
                else:
                    #If the response is not html or xml ,save the url to redis 
                    pass
        except requests.ConnectTimeout,e:
            print('Connect %s timeout .\n%s' % (url,str(e)))
            if self._redis_enable:
                self._r.get_redis().lpush(self._start,url)
        except requests.ConnectionError,e2:
            print('Connect %s error.\n%s' % (url,str(e2)))
        except Exception,e3:
            print('Connect %s error.\n%s' % (url,str(e3)))
            self._r.get_redis().sadd('parsed_'+self._start,url)

    def _get_url(self,url):
        '''
        Get url from redis by the given url
        '''
        parsed_url='parsed_'+url

        if self._redis_enable:
            get_url=urlparse.urljoin(self._start,self._r.get_redis().lpop(url))
            while self._r.get_redis().sismember(parsed_url,urlparse.urljoin(self._start,get_url)):
                get_url=self._r.get_redis().lpop(url)
            #self._r.get_redis().sadd(url,get_url)
            if get_url:
                return urlparse.urljoin(self._start,get_url)
            else:
                #import sys
                #sys.exit(-1)
                return None
        else:
            return None




    def _get_content_encoding(self,content_type):
        '''
        Get content encoding from content-type
        '''
        regx=re.compile('(?<=charset\=).*')
        return regx.findall(content_type)

    def run(self):
        print 'Starting crawling'
        self._log.debug('Starting crawling %s ' % self._start)
        url=self._start
        while True:
            print('Crawling %s ' % url)
            if url:
                print('parsing %s ' % url)
                self._get_response(url=url)
                print('parsed %s ' % url)
            url=self._get_url(self._start)
            self._log.debug('get url %s from redis' % url)
            print('get new url from redis:%s' % url)
            time.sleep(3)






