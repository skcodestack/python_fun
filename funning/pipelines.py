# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import scrapy
from scrapy  import log
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from hashlib import md5
import MySQLdb
from twisted.enterprise import adbapi
import datetime
import MySQLdb
import MySQLdb.cursors
import logging 

logger=logging.getLogger("shikai")

class MySQLStorePipeline(object):
	'''
	linkmd5id   | char(32) | NO   | PRI | NULL    |       |
	| title       | text     | YES  |     | NULL    |       |
	| content | text     | YES  |     | NULL    |       |
	| image_url   | text     | YES  |     | NULL    |       |
	| updated     | datetime | YES  |     | NULL    
	   item
	'''
	def __init__(self,dbpool):
		# dbargs = dict(
		# 	host=settings['MYSQL_HOST'],
		# 	db=settings['MYSQL_DBNAME'],
		# 	user=settings['MYSQL_USER'],
		# 	passwd=settings['MYSQL_PASSWD'],
		# 	charset='utf8',
		# 	cursorclass = MySQLdb.cursors.DictCursor,
		# 	use_unicode= True,
		# )
		# dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
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

	#pipeline默认调用
	def process_item(self, item, spider):
		logger.info("===>process_item")
		d = self.dbpool.runInteraction(self._do_upinsert, item, spider)
		d.addErrback(self._handle_error, item, spider)
		# d.addBoth(lambda _: item)
		return d
	#将每行更新或写入数据库中
	def _do_upinsert(self, conn, item, spider):
		linkmd5id = self._get_linkmd5id(item)
		logger.info("===>_do_upinsert"+linkmd5id+";;;;;;")
		print "=====>"+linkmd5id
		# now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
		now = datetime.datetime.now()
		conn.execute("""
		select 1 from imagesinfo where linkmd5id = %s
		""", (linkmd5id, ))
		ret = conn.fetchone()
		#linkmd5id     title     content     image_url  updated item  path
		if ret:
			logger.info("===>_do_upinsert1111111111111111111111")
			conn.execute("""
			update imagesinfo set link_url = %s,path = %s,title = %s, content = %s, image_url = %s, item = %s, updated = %s where linkmd5id = %s
			""", (item['link_url'],item['path'],item['name'], item['content'], item['src_url'], item['item_type'], now, linkmd5id))
		#print """
		#    update cnblogsinfo set title = %s, description = %s, link = %s, listUrl = %s, updated = %s where linkmd5id = %s
		#""", (item['title'], item['desc'], item['link'], item['listUrl'], now, linkmd5id)
		else:
			logger.info("===>_do_upinsert22222222222222222")
			conn.execute("""
			insert into imagesinfo(linkmd5id, link_url,title, content, image_url, path, updated,item) 
			values(%s, %s, %s, %s, %s, %s, %s, %s)
			""", (linkmd5id, item['link_url'],item['name'], item['content'], item['src_url'], item['path'], now,item['item_type']))


	#print """
	#    insert into cnblogsinfo(linkmd5id, title, description, link, listUrl, updated)
	#    values(%s, %s, %s, %s, %s, %s)
	#""", (linkmd5id, item['title'], item['desc'], item['link'], item['listUrl'], now)
	#获取url的md5编码
	def _get_linkmd5id(self, item):
		#url进行md5处理，为避免重复采集设计
		return md5(item['link_url']).hexdigest()
	#异常处理
	def _handle_error(self, failue, item, spider):
		# log.error_message=''
		log.err(failue)

 # class SQLStorePipeline(object):
        
	# def __init__(self):
	# 	self.dbpool = adbapi.ConnectionPool('MySQLdb', db='mydb',
	# 	user='myuser', passwd='mypass', cursorclass=MySQLdb.cursors.DictCursor,
	# 	charset='utf8', use_unicode=True)

	# def process_item(self, item, spider):
	# 	# run db query in thread pool
	# 	query = self.dbpool.runInteraction(self._conditional_insert, item)
	# 	query.addErrback(self.handle_error)

	# 	return item

	# def _conditional_insert(self, tx, item):
	# 	# create record if doesn't exist.
	# 	# all this block run on it's own thread
	# 	tx.execute("select * from websites where link = %s", (item['link'][0], ))
	# 	result = tx.fetchone()
	# 	if result:
	# 		log.msg("Item already stored in db: %s" % item, level=log.DEBUG)
	# 	else:
	# 		tx.execute(\
	# 		"insert into websites (link, created) "
	# 		"values (%s, %s)",
	# 		(item['link'][0],
	# 		datetime.datetime.now())
	# 		)
	# 		log.msg("Item stored in db: %s" % item, level=log.DEBUG)

	# def handle_error(self, e):
	# 	log.err(e)
                                                                                                                                                                            
class FilePipeline(FilesPipeline):
	'''
		file  download
	'''
	def get_media_requests(self, item, info):
		image_url = item['src_url']
		if   'http://www.zbjuran.com' not in  image_url:
			image_url="http://www.zbjuran.com"+image_url
			item['src_url']=image_url
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
	'''
		save  json file
	'''
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
	 	

