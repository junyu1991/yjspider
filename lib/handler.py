#!/usr/bin/env python
#!encoding:utf-8

from bs4 import BeautifulSoup
import redis_tool

class Resp_Handler():

    def __init__(self,handler_name="",redis_config='redis-config.json'):
        self.name=handler_name



    def get_soup(self,data):
        self._soup=BeautifulSoup(data,'lxml')

    def handle_data(self,response):
        self.get_soup(response.text)
        self._url=response.url

        self.handle_link()
        self.handle_img()
        self.handle_static_files()
        self.handle_html()
        return None

    def handle_link(self):
        a_link=[a.get('href') for a in self._soup.find_all('a') if a.get('href')]

    def handle_img(self):
        img_link=[img.get('src') for img in self._soup.find_all('img') if img.get('src')]

    def handle_static_files(self):
        js=[sc.get('src') for sc in self._soup.find_all('script') if sc.get('src')]
        css=[cs.get('href') for cs in self._soup.find_all('link') if cs.get('href')]

