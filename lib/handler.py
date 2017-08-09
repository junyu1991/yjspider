#!/usr/bin/env python
#!encoding:utf-8

from bs4 import BeautifulSoup
import redis_tool
import tools
import urlparse

class Resp_Handler():

    def __init__(self,handler_name="",redis_config='redis-config.json'):
        self.name=handler_name
        self._log=tools.My_Log(logfile='resp_handler')
        self._init_redis(redis_config)


    def _init_redis(self,redis_config):
        self._log.debug('Init redis')
        self._redis=redis_tool.redis_tool(redis_config)
        self._redis_enable=self._redis.get_init_status()
        if self._redis_enable:
            self._r=self._redis.get_redis()
            self._log.debug("Init redis success")
        else:
            self._log.warning('Init redis failed')

    def get_soup(self,data):
        '''
        data=data.decode('utf-8').encode('utf-8')
        with open('text.txt','wb') as f:
            f.write(data)
        '''
        self._soup=BeautifulSoup(data,'lxml')
        #print(self._soup.find_all('img'))

    def handle_data(self,response):
        self.get_soup(response.content)
        response.close()
        url=response.url
        self._log.debug('parsing %s' % url)
        self.handle_link()
        self.handle_img()
        self.handle_static_files()
        self.handle_html()

        #Update parsed url database
        parsed='parsed_'+self.name
        if self._redis_enable:
            self._r.sadd(parsed,url)
        return None

    def handle_link(self):
        a_link=[a.get('href') for a in self._soup.find_all('a') if a.get('href')]
        if not self._redis_enable:
            return
        self._log.debug("putting url into redis %s " % self.name)
        for a_l in a_link:
            pass
            self._r.lpush(self.name,a_l)

    def handle_img(self):
        img_link=[img.get('src') for img in self._soup.find_all('img') if img.get('src')]
        #print img_link
        if not self._redis_enable:
            return
        download_url='download_'+self.name
        self._log.debug('putting download url to %s ' % download_url)
        print ("putting to %s " % download_url)
        for i_l in img_link:
            #print(i_l)
            self._r.lpush(download_url,i_l)

    def handle_static_files(self):
        js=[sc.get('src') for sc in self._soup.find_all('script') if sc.get('src')]
        css=[cs.get('href') for cs in self._soup.find_all('link') if cs.get('href')]
    
    def handle_html(self):
        pass
