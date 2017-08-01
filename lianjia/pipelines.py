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

class JsonPipeline(object):
    def __init__(self):
	num = self.getIdfromfile()
        self.file = codecs.open('/home/jasson/lianjia_'+num+'.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()

    def getIdfromfile()
	item = json.loads("/home/jasson/links")
        with open("./data/"+f) as json_file:
             for line in json_file:
		item = json.loads(line)
		if item["done"]=="yes":
			continue
		else:
			return item["id"]
			
		#	return
