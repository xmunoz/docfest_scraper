# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
from scrapy import log

class DocfestPipeline(object):
    def process_item(self, item, spider):
        log.msg(pformat(item), level=log.DEBUG)
        return item
