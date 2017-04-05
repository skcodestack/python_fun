# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from funning.items import GifItem
import scrapy
import urllib
import time
import re


# page_lx = LinkExtractor(allow=('list_4_\d+\.html'))
# print html.xpath('//div[@class="item"]//h3/a/b')[0].text
#  html.xpath('//div[@class="text"]/..//h3/a/b')[0].text
#  print  html.xpath('//div[@class="text"]/..//h3/a/b')[0].text

class funningSpider(CrawlSpider):
	name = 'funningSpider'
	num = 0
	allow_domain = ['http://www.zbjuran.com']
	start_urls = [
		'http://www.zbjuran.com/dongtai/list_4_1.html',
		'http://www.zbjuran.com/xiegif/list_18_1.html',
		'http://www.zbjuran.com/quweitupian/list_2_1.html',
		'http://www.zbjuran.com/wenzixiaohua/list_1_1.html'
	]

	rules = {
		# Rule(LinkExtractor(allow='page'), process_links='process_request', follow=True), ,follow=True
		Rule(LinkExtractor(allow='dongtai/list_4_\d+\.html$'), callback='dongtai_parse_content',follow=True),
		Rule(LinkExtractor(allow='xiegif/list_18_\d+\.html$'), callback='xiegif_parse_content',follow=True),
		Rule(LinkExtractor(allow='quweitupian/list_2_\d+\.html$'), callback='image_parse_content',follow=True),
		Rule(LinkExtractor(allow='wenzixiaohua/list_1_\d+\.html$'), callback='text_parse_content',follow=True)
	}

	def dongtai_parse_content(self , response):
		for site in response.xpath('//div[@class="text"]'):
			item=GifItem()
			item['item_type']='0'
			item['content']='  '
			item['path']='  '
			try :
				item['link_url']=site.xpath('./..//h3/a/@href').extract()[0]
				item['name']=site.xpath('./..//h3/a/b/text()').extract()[0]
				item['src_url']=site.xpath('./p/img/@src').extract()[0]
			except Exception,ex:
				item['name']=' '
				item['src_url']=' '
				pass
			# print item['name'],item['src_url']
			yield item



	def xiegif_parse_content(self , response):
		for site in response.xpath('//div[@class="text"]'):
			item=GifItem()
			item['item_type']='1'
			item['content']='  '
			item['path']='  '
			try :
				item['link_url']=site.xpath('./..//h3/a/@href').extract()[0]
				item['name']=site.xpath('./..//h3/a/b/text()').extract()[0]
				item['src_url']=site.xpath('./p/img/@src').extract()[0]
			except Exception,ex:
				item['name']=' '
				item['src_url']=' '
				pass
			# print item['name'],item['src_url']
			yield item
	def image_parse_content(self , response):
		for site in response.xpath('//div[@class="text"]'):
			item=GifItem()
			item['item_type']='2'
			item['content']='  '
			item['path']='  '
			try :
				item['link_url']=site.xpath('./..//h3/a/@href').extract()[0]
				item['name']=site.xpath('./..//h3/a/b/text()').extract()[0]
				item['src_url']=site.xpath('./p/img/@src').extract()[0]
			except Exception,ex:
				item['name']=' '
				item['src_url']=' '
				pass
			# print item['name'],item['src_url']
			yield item
	

	def text_parse_content(self , response):
		for site in response.xpath('//div[@class="text"]'):
			item=GifItem()
			item['item_type']='3'
			item['name']=' '
			item['src_url']=' '
			item['path']='  '
			try :
				item['link_url']=site.xpath('./..//h3/a/@href').extract()[0]
				item['name']=site.xpath('./..//h3/a/b/text()').extract()[0]
				item['content']=site.xpath('./p/a/text()').extract()[0]
			except Exception,ex:
				item['name']=' '
				item['content']=' '
				pass
			# print item['name'],item['content']
			yield item