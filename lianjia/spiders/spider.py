#coding:utf-8
import scrapy
import redis
import MySQLdb as mdb
from fake_useragent import UserAgent
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from lianjia.items import LianjiaItem
class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    download_delay = 3.0
    ua = UserAgent()
    conn = mdb.connect("localhost","root","123456")
    # custom_settings = {'HTTPCACHE_ENABLED': True}
    start_urls = ['https://bj.lianjia.com/ershoufang/pinggu']

    #rules = (
    #    Rule(SgmlLinkExtractor(allow='/chengjiao/pinggu/'), callback='next_page'),
   # )

    def parse(self, response):

        page_url = response.xpath('//@page-url').extract_first()
	print "the resonse url is:" + page_url
        page_data = response.xpath('//@page-data').extract_first()
        total_page = eval(page_data)['totalPage']
        total_page = 1
        for page in range(1, total_page + 1):
            rel_url = page_url.format(page=page)
            item = scrapy.Request(url=response.urljoin(rel_url), callback=self.parse_item,
                                 headers={'User-Agent': self.ua.random})
	    return item

    def parse_item(self, response):
          for house in response.xpath('//ul[@class="sellListContent"]/li'):
            l = ItemLoader(item=LianjiaItem(), response=response, selector=house)
            l.default_output_processor = Join()
            l.add_xpath('title', './/div[@class="title"]/a/text()')
            l.add_xpath('community', './/div[@class="houseInfo"]/a/text()')
            l.add_xpath('model', './/div[@class="houseInfo"]/text()', re=r'\d室\d厅')
            l.add_xpath('area', './/div[@class="houseInfo"]/text()', re=r'[\d\.]+平米')
            l.add_xpath('direction', './/div[@class="houseInfo"]/text()', re=r'[东西南北]+')
            l.add_xpath('decoration', './/div[@class="houseInfo"]/text()', re=r'.装')
            l.add_xpath('focus_num', './/div[@class="followInfo"]/text()', re=r'\d+人关注')
            l.add_xpath('watch_num', './/div[@class="followInfo"]/text()', re=r'共\d+次带看')
            l.add_xpath('time', './/div[@class="followInfo"]/text()', re=r'\d+[天月个]以前发布')
            l.add_xpath('price', './/div[@class="totalPrice"]/span/text()')
            l.add_xpath('average_price', './/div[@class="unitPrice"]/@data-price')
            l.add_xpath('link', './/div[@class="title"]/a/@href')
            item = l.load_item()
            yield item


#if __name__ == '__main__':
#    from scrapy import cmdline

 #   cmdline.execute('scrapy runspider lianjia_bj.py'.split())
