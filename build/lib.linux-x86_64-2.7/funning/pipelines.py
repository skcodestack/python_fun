# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class FilePipeline(FilesPipeline):
	def get_media_requests(self, item, info):
		image_url = item['src_url']
		if   'http://www.zbjuran.com' not in  image_url:
			image_url="http://www.zbjuran.com"+image_url
		print image_url
		yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):
		if item['item_type'] == '0' or item['item_type'] == '1'  or item['item_type'] == '2':
			image_paths = [x['path'] for ok, x in results if ok]
			if not image_paths:
				raise DropItem("Item contains no images")
			item['path'] = image_paths[0]
		return item

class FunningPipeline(object):
	def __init__(self):
		self.file=codecs.open('gif_item.json','w',encoding='utf-8')
		self.xiefile=codecs.open('xie_item.json','w',encoding='utf-8')
		self.imagefile=codecs.open('image_item.json','w',encoding='utf-8')
		self.textfile=codecs.open('text_item.json','w',encoding='utf-8')

	def process_item(self, item, spider):
		print item['item_type']
		if item['item_type'] == '0':
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			self.file.write(line)
		elif item['item_type'] == '1':
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			self.xiefile.write(line)
		elif item['item_type'] == '2':
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			self.imagefile.write(line)
		elif item['item_type'] == '3':
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			self.textfile.write(line)
		return item


	def spider_closed(self,spider):
	 	self.file.close()
	 	self.xiefile.close()
	 	self.imagefile.close()
	 	self.textfile.close()
	 	

