# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FunningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class GifItem(scrapy.Item):
	# define the fields for your item here like:
	'''
	0---gif
	1--xiee
	2--images
	3---text
	'''
	item_type = scrapy.Field()
	name = scrapy.Field()
	src_url = scrapy.Field()
	content = scrapy.Field()
	path=scrapy.Field()
	pass
