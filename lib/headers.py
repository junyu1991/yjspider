#!/usr/bin/env python
#!encoding:utf-8

import re

regx=re.compile('((e|E)xpires|(p|P)ath|(d|D)omain|(m|M)ax-age)')

class header():

    def __init__(self,*args):
        self.args=args
        self._header={"Accept":"text/plain","Accept-Charset":"utf-8",\
                       "Connection":"keep-alive"
                      }
        self._useragent={"Chrome":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",\
                          "Opera":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41",\
                          "Safari":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1",\
                          "IE":'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)',\
                          "GoogleCrawler":"Googlebot/2.1 (+http://www.google.com/bot.html)",\
                          "FireFox":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
                         }
        self._header['User-Agent']=self.get_ua()

    def get_request_header(self,Cookie="",Refer="",**args):
        '''
        Return the request header
        @param:Cookie :the requests cookie
        @param:Refer the request refer param
        @args:other requests param like X-Requestde-With
        @return:request header
        '''
        temp_header=self._header.copy()
        if Cookie:
            temp_header['Cookie']=Cookie
        if Refer:
            temp_header['Refer']=Refer
        temp_header['User-Agent']=self.get_ua()

        for k,v in args.items():
            temp_header[k]=v

        return temp_header

    def set_default_header(self,header={}):
        '''
        Set default request header
        @param:the request header want to be set
        @return:None
        '''
        self._header=header.copy()

    def update_header(self,param={}):
        '''
        Update the default header
        @param:param the param you want to update
        @return:None
        '''
        for k,v in param.items():
            self._header[k]=v

    def get_default_header(self):
        '''
        Get default requests header
        @param:
        @return:default requests header
        '''
        return self._header.copy()

    def get_ua(self,explorer='IE'):
        '''
        Get User-Agent
        @param:Explorer version
        @return:return user agent
        '''
        return self._useragent.get(explorer)

    def parse_header(self,response_header={}):
        '''
        Parse response header,now this function just reset the cookie and connection if the response header has the key "Set-Cooike" and "Conncetion"
        @param:response header
        @return:None
        '''
        if response_header.has_key('Set-Cookie'):
            self._header['Cookie']=response_header.get('Set-Cookie')
        if response_header.has_key('Connection'):
            self._header['Connection']=response_header.get('Connection')

def get_cookie(set_cookie=''):
    cookie=''
    for sc in set_cookie.split():
        temp=sc.split('=')
        if len(temp)>1 and not regx.search(temp[0]):
            cookie+=sc
    return cookie


if __name__=='__main__':
    set_cookie='fixed_bar=1; expires=Mon, 25-Sep-2017 23:59:59 GMT; path=/, TIEBAUID=cb23caae14130a0d384a57f1; expires=Thu, 31-Dec-2020 15:59:59 GMT; path=/; domain=tieba.baidu.com'
    set_cookie='BAIDUID=009676F5281D7B98715CD0E38FB1F5DC:FG=1; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com, BIDUPSID=009676F5281D7B98715CD0E38FB1F5DC; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/;domain=.baidu.com, PSTM=1506321109; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com, BDSVRTM=0; path=/, BD_HOME=0; path=/, H_PS_PSSID=1430_21123_18559_22073; path=/; domain=.baidu.com'
    print get_cookie(set_cookie)



