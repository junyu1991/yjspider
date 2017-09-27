#!/usr/bin/env python
#!encoding:utf-8

from yjspider import *

from lib import download
from lib import handler
from lib import codes
import urlparse

if __name__=='__main__1':
    '''
    yj=yjspider(redis_config='./config/redis-config.json')
    url='http://jandan.net/ooxx'
    yj.start(url=url)
    '''

    test_resp()
    d=download.Download(redis_config='./config/redis-config.json',download_url=url)
    #d.run()




class my_handler(handler.Resp_Handler):
    def handle_link(self):
        #ownload_url=self._r.hget(self.name,codes.url)
        a_link=[a.get('href') for a in self._soup.find_all('a') if a.get('href')]
        a_link=list(set(a_link))
        b_link=[]
        for a in a_link:
            a=urlparse.urldefrag(a)[0]
            if a.startswith('//jandan.net/ooxx') or a.startswith('//wx1.sinaimg.cn'):
                print("Putting %s " % (a))
                #self._r.lpush(download_url,a)
                b_link.append(a)
        self._add_link(b_link)


def test_resp():
    url=''
    url='http://jandan.net/ooxx'
    #yj=yjspider(redis_config='./config/redis-config.json')
    yj=yjspider(redis_config='./config/redis-config.json')
    myhand=my_handler()
    myhand.name=url
    yj.set_resp_handler(myhand)
    yj.start(url=url)

def test_download():
    d=download.Download(redis_config='./config/redis-config.json',download_url='http://jandan.net/ooxx')
    d.run()

if __name__=='__main__':
    test_resp()
    #test_download()
