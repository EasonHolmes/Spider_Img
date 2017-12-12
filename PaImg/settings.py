# -*- coding: utf-8 -*-

# Scrapy settings for PaImg project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'PaImg'

SPIDER_MODULES = ['PaImg.spiders']
NEWSPIDER_MODULE = 'PaImg.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'PaImg (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# 除非您 真的 需要，否则请禁止cookies。在进行通用爬取时cookies并不需要， (搜索引擎则忽略cookies)。禁止cookies能减少CPU使用率及Scrapy爬虫在内存中记录的踪迹，提高性能。
COOKIES_ENABLED = False  # 禁用cookie
IMAGES_STORE = '/Users/cuiyang/Pictures/meizitu'  # 设置图片保存目录本地
# 设置保存目录为上传路径可自动上传
# Amazon S3 storage
# FILES_STORE and IMAGES_STORE can represent an Amazon S3 bucket. Scrapy will automatically upload the files to the bucket.
# For example, this is a valid IMAGES_STORE value:
# IMAGES_STORE = 's3://bucket/images'
# You can modify the Access Control List (ACL) policy used for the stored files, which is defined by the FILES_STORE_S3_ACL and IMAGES_STORE_S3_ACL settings. By default, the ACL is set to private. To make the files publicly available use the public-read policy:
# IMAGES_STORE_S3_ACL = 'public-read'
# For more information, see canned ACLs in the Amazon S3 Developer Guide.
#


# 对失败的HTTP请求进行重试会减慢爬取的效率，尤其是当站点响应很慢(甚至失败)时， 访问这样的站点会造成超时并重试多次。这是不必要的，同时也占用了爬虫爬取其他站点的能力。
RETRY_ENABLED = False
# 减小下载超时:
# 如果您对一个非常慢的连接进行爬取(一般对通用爬虫来说并不重要)， 减小下载超时能让卡住的连接能被快速的放弃并解放处理其他站点的能力。
DOWNLOAD_TIMEOUT = 15
# 启用 “Ajax Crawlable Pages” 爬取
# 有些站点(基于2013年的经验数据，之多有1%)声明其为 ajax crawlable 。 这意味着该网站提供了原本只有ajax获取到的数据的纯HTML版本。 网站通过两种方法声明:
# 在url中使用 #! - 这是默认的方式;
# 使用特殊的meta标签 - 这在”main”, “index” 页面中使用。
# Scrapy自动解决(1)；解决(2)您需要启用 AjaxCrawlMiddleware:
# AJAXCRAWL_ENABLED = True
# 通用爬取经常抓取大量的 “index” 页面； AjaxCrawlMiddleware能帮助您正确地爬取。 由于有些性能问题，且对于特定爬虫没有什么意义，该中间默认关闭。
AJAXCRAWL_ENABLED = False
# 滤出小图片
# 你可以丢掉那些过小的图片，只需在 IMAGES_MIN_HEIGHT 和 IMAGES_MIN_WIDTH 设置中指定最小允许的尺寸。
IMAGES_MIN_HEIGHT = 110
IMAGES_MIN_WIDTH = 110

IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}
# 是否启用logging。
# LOG_ENABLED = True
# log打印格式
# LOG_FORMAT = '%(asctime)s,%(msecs)d  [%(name)s] %(levelname)s: %(message)s'


# 保存项目中启用的pipeline及其顺序的字典。该字典默认为空，值(value)任意。不过值(value)习惯设定在0-1000范围内。
# 注释ITEM_PIPELINES中的内容是因为在Spider中定义了单独每个Spider处理数据需要用的item pipelines，而不是共用一个。
# 如果你的item pipelines是Spider可以共用的则可以定义在settings.py中
# 举个例子，假如有两个Spider，Spider A在进行数据处理时只想执行的是pipeline A中的方法，Spider B只想执行的是pipeline B中的方法。
# 如果在settings.py中定义了的话，pipeline A或者B都会被执行到。这样不是我们想要的结果。
# 所以可以在spider中单独定义。可以看第四篇文章的第三节“爬取规则”中的代码。
# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
# http://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/item-pipeline.html
ITEM_PIPELINES = {
    'PaImg.pipelines.PaimgPipeline': 300,
}
# 要激活下载器中间件组件，将其加入到 DOWNLOADER_MIDDLEWARES 设置中。
# 该设置是一个字典(dict)，键为中间件类的路径，值为其中间件的顺序(order)。
# 网站时，网站会对IP会有限制，如果一段时间内同一ip访问请求过多。服务端的http响应会直接返回503的error code。
# 所以我们必须编写一些下载器中间件来应对这样的限制。同时我们也需要自己建立一个ip代理池来为爬虫中的http请求维护可用的代理ip。

# CustomUserAgentMiddleware：在每个http请求的请求头中添加User-Agent。
# CustomHttpProxyMiddleware：在每个http请求的请求头中添加代理ip，使得Scrapy的下载器在下载网页数据时都是通过代理IP来下载。
# CatchExceptionMiddleware：如果一个http请求出错或失败了，那么在ip代理池中添加一次该代理ip失败的记录。
#  代理IP可能会失效 需要重新ping代理ip地址
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'PaImg.RandomUserAgent.RandomUserAgent': 100,

     # 代理IP可能会失效 需要重新ping代理ip地址
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware' : None,
    # 'PaImg.ProxiesMiddleware.ProxiesMiddleware' : 100
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# Scrapy downloader 并发请求(concurrent requests)的最大值。
CONCURRENT_REQUESTS = 12
# Twisted模块中Reactor最大线程池数量。
REACTOR_THREADPOOL_MAXSIZE = 8

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 下载器在下载同一个网站下一个页面前需要等待的时间。该选项可以用来限制爬取速度， 减轻服务器压力。同时也支持小数:
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

# IPPOOL=[
#     {"ipaddr":"211.142.141.210:8998"},
#     {"ipaddr":"58.19.15.218:808"},
#     {"ipaddr":"117.90.1.141:9000"},
#     {"ipaddr":"125.117.115.180:9000"},
#     {"ipaddr":"211.142.141.210:8998"},
#     {"ipaddr":"163.125.251.242:8118"}
# ]
# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,applicatioST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Lan/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'PaImg.middlewares.PaimgSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'PaImg.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }



# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
