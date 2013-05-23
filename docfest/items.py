# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class DocfestItem(Item):
    date = Field()
    doc_title = Field()
    venue = Field()
    start_time = Field()
    duration = Field()
    description = Field()
    info_link = Field()
