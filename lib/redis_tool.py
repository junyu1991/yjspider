#!/usr/bin/env python
#!encoding:utf-8

import redis
import os
import json
import sys

class redis_tool():

    def __init__(self,config_file):
        config_data=get_config(config_file)
        if config_data:
            host=config_data.get('host')
            port=config_data.get('port')
            password=config_data.get('password')
            db=config_data.get('db')
            self.init_redis(host,port,password,db)
        else:
            print("Redis init failed.Existing")
            self._is_init=False


    def init_redis(self,host,port,password,db):
        pool=redis.ConnectionPool(host=host,port=port,password=password,db=db)
        self._r=redis.Redis(connection_pool=pool)
        try:
            self._r.setnx('test','test')
            self._is_init=True
        except redis.RedisError,e:
            print("Redis init failed: %s" % str(e))
            self._is_init=False

    def get_init_status(self):
        return self._is_init

    def get_redis(self):
        return self._r


def get_config(config_file):
    data={}
    if os.path.exists(config_file):
        with open(config_file,'rb') as f:
            data=json.load(f)
    else:
        temp_dir=os.path.abspath(__file__)
        temp_dir=os.path.join(os.path.dirname(os.path.dirname(temp_dir)),'config')
        config_dir=os.path.join(temp_dir,config_file)
        with open(config_dir,'rb') as f:
            data=json.load(f)
    return data


