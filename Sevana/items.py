# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PensionerItem(scrapy.Item):
    # define the fields for your item here like:
    pensioner_id = scrapy.Field()
    pensioner_name = scrapy.Field()
    pension_type = scrapy.Field()
    address = scrapy.Field()
    gender = scrapy.Field()
    last_disbursed_month = scrapy.Field()
    pass


class BplItem(Scrapy>Item): 
	name= scrapy.Field()
    pass