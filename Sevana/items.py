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


class BplItem(scrapy.Item): 
	i1= scrapy.Field()
	i2= scrapy.Field()
	i3= scrapy.Field()
	i4= scrapy.Field()
	i5= scrapy.Field()
	i6= scrapy.Field()
	i7= scrapy.Field()
	i8= scrapy.Field()
	i9= scrapy.Field()
	pass