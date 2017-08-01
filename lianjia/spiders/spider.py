#coding:utf-8
import scrapy
import time
import random
#import redis
#import MySQLdb as mdb
from fake_useragent import UserAgent
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from lianjia.items import LianjiaItem
class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    download_delay = 3.0
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]


    ua = UserAgent()
#    ua = random.choice(user_agent_list)
 #   if ua:
  #        request.headers.setdefault('User-Agent', ua)
#    conn = mdb.connect("localhost","root","123456")
    # custom_settings = {'HTTPCACHE_ENABLED': True}
    #start_urls = ['https://bj.lianjia.com/chengjiao/andingmen']
    #start_urls = ['https://bj.lianjia.com/chengjiao/anzhen1/p1p2p3p4']
    #start_urls = ['https://bj.lianjia.com/chengjiao/anzhen1/p5p6p7p8']
    #start_urls = ['https://bj.lianjia.com/chengjiao/chongwenmen']
    #start_urls = ['https://bj.lianjia.com/chengjiao/chaoyangmenwai1/']
    #start_urls = ['https://bj.lianjia.com/chengjiao/chaoyangmenwai1/']
    #start_urls = ['https://bj.lianjia.com/chengjiao/haidian/lc4lc1p1/']
    #start_urls = ['https://bj.lianjia.com/chengjiao/haidian/lc2p1/']
    currenturl = self.getCurrentUrl()
    start_urls = ['https://bj.lianjia.com/chengjiao/haidian/lc3lc5p1/']

    #rules = (
    #    Rule(SgmlLinkExtractor(allow='/chengjiao/pinggu/'), callback='next_page'),
   # )

    def parse(self, response):
        page_url = response.xpath('//@page-url').extract_first()
	print "the resonse url is:" + page_url
        page_data = response.xpath('//@page-data').extract_first()
        total_page = eval(page_data)['totalPage']
	print total_page
        #for page in range(1, total_page + 1):
        for page in range(1, 2):
            rel_url = page_url.format(page=page)
	    url = response.urljoin(rel_url)
	    print "the second request url is: "+url
            item = scrapy.Request(url=response.urljoin(rel_url), callback=self.parse_item,
                                 headers={'User-Agent': self.ua.random})
	    yield item

    def parse_item(self, response):
	  items = []
          #for house in response.xpath('//ul[@class="listContent"]/li'):
          for house in response.xpath('//div[@class="info"]'):
	    print house
            l = ItemLoader(item=LianjiaItem(), response=response, selector=house)
            l.default_output_processor = Join()
            l.add_xpath('title', './/div[@class="title"]/a/text()')
          #  l.add_xpath('community', './/div[@class="title"]/a/text()',re=r'\s+')
          #  l.add_xpath('model', './/div[@class="houseInfo"]/text()', re=r'\d室\d厅')
          #  l.add_xpath('area', './/div[@class="houseInfo"]/text()', re=r'[\d\.]+平米')
            l.add_xpath('direction', './/div[@class="houseInfo"]/text()')#, re=r'[东西南北]+')
            l.add_xpath('decoration', './/div[@class="houseInfo"]/text()', re=r'.装')
            l.add_xpath('focus_num', './/div[@class="followInfo"]/text()', re=r'\d+人关注')
            l.add_xpath('watch_num', './/div[@class="followInfo"]/text()', re=r'共\d+次带看')
            l.add_xpath('time', './/div[@class="followInfo"]/text()', re=r'\d+[天月个]以前发布')
            l.add_xpath('deal_price', './/div[@class="totalPrice"]/span/text()')
            l.add_xpath('deal_date', './/div[@class="dealDate"]/text()')
            l.add_xpath('position', './/div[@class="positionInfo"]/text()')
            l.add_xpath('average_price', './/div[@class="unitPrice"]/@data-price')
            l.add_xpath('link', './/div[@class="title"]/a/@href')
            l.add_xpath('claim_price', './/div[@class="dealCycleeInfo"]/span/span/text()')
            item = l.load_item()
	    items.append(item)
	    #print "in parse_item: "+len(items)
          return items
     def getCurrentUrl():
	item = json.loads("/home/jasson/links")
        with open("./data/"+f) as json_file:
             for line in json_file:
		item = json.loads(line)
		if item["done"]=="yes":
			continue
		else:
			return item["link"]
		

#if __name__ == '__main__':
#    from scrapy import cmdline

 #   cmdline.execute('scrapy runspider lianjia_bj.py'.split())
