#!/usr/bin/env python
#!encoding:utf-8

import urllib2
import re


from bs4 import BeautifulSoup
import requests
from headers import header
import redis_tool
from handler import Resp_Handler

class crawler():

    def __init__(self,redis_config,start_url):
        self._header=header()
        self._s=requests.Session()
        self._s.headers.update(self._header.get_default_header())
        self._handler=Resp_Handler(start_url)

    def get_response(self,url,method='get',headers={},files=[],data=None,cookies=None,cert=None,timeout=3,**kwargs):
        method=method.upper()
        self._s.headers.update(headers)
        pre=requests.Request(method=method,url=url,data=data,files=files)
        prepped=self._s.prepare_request(pre)
        with self._s.send(prepped,stream=True,cert=cert,timeout=timeout) as resp:
            self._header.parse_header(resp.headers)
            self._s.headers.update(self._header.get_default_header())
            content_type=resp.headers.get('content-type')
            encoding=self._get_content_encoding(content_type)
            regx=re.compile('.*(text\/html|text\/xml).*')
            if regx.search(content_type) and resp.status_code==requests.codes.OK:
                #Don't handle redirect url for now
                self._handler.handle(resp)
            elif resp.status_code!=requests.codes.OK:
                print("Connected url %s \t %d" % (url,resp.status_code))
            else:
                #If the response is not html or xml ,save the url to redis 
                pass

    def _get_url(self):
        '''
        Get url from redis
        '''



    def _get_content_encoding(self,content_type):
        '''
        Get content encoding from content-type
        '''
        regx=re.compile('(?<=charset\=).*')
        return regx.findall(content_type)




