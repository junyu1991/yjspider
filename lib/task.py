#!encoding:utf-8

class task:
    '''
    用于存储爬虫任务，下载任务，供多线程调用
    '''

    url_task=[]
    parsed_url=dict()

    download_task=[]
    downloaded_url=dict()

    download_path='/work/test/tempdown'
