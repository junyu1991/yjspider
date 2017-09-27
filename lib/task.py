#!encoding:utf-8

class task:
    '''
    用于存储爬虫任务，下载任务，供多线程调用
    '''

    #爬虫任务，已爬取的url
    url_task=[]
    parsed_url=dict()

    #下载器的下载任务，已下载的任务
    download_task=[]
    downloaded_url=dict()

    #下载文件存储路径
    download_path='/work/test/tempdown'
