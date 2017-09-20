# yjspider
    yjspider，基于Requests以及BeautifulSoup的小型分布式爬虫框架，使用Redis数据库进行任务分发。主要拥有三大部件：  
       1. crawler.py负责从Redis数据库中获取目标url，访问服务器，调用Resp_handler中的方法解析处理Response
       2. handler.py解析处理crawler.py中获取的Response，进行保存结果以及更新爬虫任务
       3. download.py负责下载任务，主要负责下载图片，js以及css文件
## required
>1.requests  
>2.redis  
>3.BeautifulSoup  
