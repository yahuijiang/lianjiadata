# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    community = scrapy.Field()
    model = scrapy.Field()
    size = scrapy.Field()
    direction = scrapy.Field()
    floor_num = scrapy.Field()
    decoration = scrapy.Field()
    focus_num = scrapy.Field()
    watch_num = scrapy.Field()
    time = scrapy.Field()
    deal_price = scrapy.Field()
    claim_price = scrapy.Field()
    deal_date = scrapy.Field()
    deal_duration = scrapy.Field()
    average_price = scrapy.Field()
    link = scrapy.Field()
