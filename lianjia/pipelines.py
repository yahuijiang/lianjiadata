# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
import re
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors

class LianjiaPipeline(object):

    def __init__(self, dbpool):
	self.dbpool = dbpool
    @classmethod
    def from_settings(cls, settings):
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
	    cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    def process_item(self, item, spider):
	print "we are process item"+ item["title"]
	#d = self.dbpool.runInteraction(self._do_upinsert, item, spider)	
	#d.addErrback(self._handle_error, item, spider)
	#d.addBoth(lambda _: item)
	return item

    #将每行更新或写入数据库中
    def _do_upinsert(self, conn, item, spider):
	print item
    def ii_do_upinsert(self, conn, item, spider):
	#print linkmd5id
	print "we are writing sql azure"
	print item
	if item["position"]==None or item['position']==None or item['claim_price'] ==None or item['direction']==None: 
		return
	#print item["deal_price"]
	#print "direction: "+item["direction"]
	#print ("""
	#    insert into lianjiahistory(link, title, description) 
        #    values(%s, %s, %s)
	#    """, (item['title'], item['deal_price'], item['link']))
	try:
		titlereg = re.compile(r'\s')
		titleinfo = titlereg.split(item['title'])
		community = titleinfo[0]
		model = titleinfo[1]
		area = titleinfo[2]
		positioninfo = titlereg.split(item['position'])
		print positioninfo[0]
		floor=positioninfo[0]
		time=positioninfo[1]
		dealinfo = titlereg.split(item['claim_price'])
		print dealinfo[0]
		claim_price=dealinfo[0]
		deal_duration=dealinfo[1]
	        directionreg = re.compile(r'\|')
                dirinfo = directionreg.split(item['direction'])	
		print dirinfo
		conn.execute("""
		    insert into lianjiahistory(title,deal_price,deal_date,community,model,floor_num,time,deal_duration,claim_price,direction,decoration,area) 
		    values(%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
		    """, (item['title'], item['deal_price'],item['deal_date'],community, model,floor,time,deal_duration,claim_price,dirinfo[0],dirinfo[1],area))
        except Exception, e:
          print 'str(Exception):\t',e.message 
          print 'sn):\t',traceback.print_exc() 
	    #获取url的md5编码	
    def _get_linkmd5id(self, item):
	#url进行md5处理，为避免重复采集设计
	return md5(item['link']).hexdigest()
    #异常处理
    def _handle_error(self, failue, item, spider):
	log.err(failure)  
