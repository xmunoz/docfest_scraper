#!/usr/bin/env python

# Imports
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from docfest.items import DocfestItem
from scrapy import log
import unicodedata
from pprint import pformat
from scrapy.conf import settings
from datetime import date, timedelta
from urllib import quote_plus
from time import sleep

def fetch_dates():
    start_date = date(2013, 5, 28)
    end_date = date(2013, 5, 30)
    num_days = (end_date - start_date).days
    dates = [start_date + timedelta(days=x) for x in range(0,num_days)]
    return dates

def construct_start_urls(datetime_dates):
    url_prefix = 'http://prod3.agileticketing.net/websales/pages/list.aspx?epguid=5e3ea987-8f29-408f-ad74-5c32388b1f83&view=simple&mdyr='
    url_suffix = '~0&'
    urls = []
    for date in datetime_dates:
        date_str = quote_plus(" ".join([str(date.month), str(date.day), str(date.year)]))
        urls.append("".join([url_prefix, date_str, url_suffix]))
    return urls

class DocfestSpider(BaseSpider):
    name = "dfs"
    allowed_domains = ["prod3.agileticketing.net"]
    dates = fetch_dates()
    start_urls = construct_start_urls(dates)

    def parse(self, response):
        '''
        Parse http response
        '''
        hxs = HtmlXPathSelector(response)
        sleep(1)
        no_screenings = hxs.select('//*[@id="ctl00_CPH1_lblNothingToList"]').extract()
        if no_screenings:
            log.msg('No screenings', level=log.INFO)
            return None
        else:
            return self._get_screenings(hxs, response)

    def _get_screenings(self, hxs, response):
        screenings = hxs.select('//*[@class="Item"]')
        for screening in screenings:
            log.msg(pformat(screening.extract()))
            item = DocfestItem()
            self._set_date(item, response)
            self._set_doc_title(item, screening)
            self._set_venue(item, screening)
            self._set_start_time(item, screening)
            self._set_duration(item, screening)
            self._set_description(item, screening)
            self._set_info_link(item, screening)
            yield item

    def _set_date(self, item, response):
        log.msg(pformat(response), level=log.INFO)
    
    def _set_doc_title(self, item, screening):
        title = screening.select('//*[@class="Name"]/text()').extract()
        log.msg(pformat(title), level=log.INFO)
        item['doc_title'] = self._format_output(title) if title else None
    
    def _set_venue(self, item, screening):
        venue = screening.select('//*[@class="Venue"]/a/text()').extract()
        item['venue'] = self._format_output(screening) if venue else None 

    def _set_start_time(self, item, screening):
        start_time = screening.select('//*[@class="EventDate"]/text()').extract()
        item['start_item'] = self._format_output(start_time) if start_time else None 
    
    def _set_duration(self, item, screening):
        duration = screening.select('//*[@class="EventDuration"]/text()').extract()
        item['duration'] = self._format_output(duration) if duration else None 

    def _set_description(self, item, screening):
        description = screening.select('//*[@class="Descriptive ShortDescription"]/text()').extract()
        item['description'] = self._format_output(description) if description else None 
    
    def _set_info_link(self, item, screening):
        info_link = screening.select('//*[@class="DescriptionContainer"]/a/href()').extract()
        item['info_link'] = self._format_output(info_link) if info_link else None 
    
    def _format_output(self, unicode_str):
        '''
        Takes a unicode string, and converts it to ascii. Strips trailing and leading whitespace and newlines.
        '''
        ascii_str = unicodedata.normalize('NFKD', unicode_str).encode('ascii','ignore')
        return ascii_str.strip()

    
