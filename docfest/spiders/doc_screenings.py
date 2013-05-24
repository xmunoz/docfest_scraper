#!/usr/bin/env python

# Imports
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from docfest.items import DocfestItem
from scrapy import log
import unicodedata
from pprint import pformat
from scrapy.conf import settings
from datetime import date, timedelta, time
from urllib import quote_plus
from scrapy.http import Request

def fetch_dates():
    '''
    Construct list of dates
    '''
    start_date = date(2013, 5, 28)
    end_date = date(2013, 6, 30)
    num_days = (end_date - start_date).days
    dates = [start_date + timedelta(days=x) for x in range(0,num_days)]
    return dates

def construct_start_urls(datetime_dates):
    '''
    Construct list of urls to scrape based on dates
    '''
    #the epguid param needs to be refreshed every 10 minutes or so (simply copy/paste from a browser)
    url_prefix = 'http://prod3.agileticketing.net/websales/pages/list.aspx?epguid=5e3ea987-8f29-408f-ad74-5c32388b1f83&view=simple&mdyr='
    url_suffix = '~0&'
    urls = []
    for date in datetime_dates:
        date_str = quote_plus(" ".join([str(date.month), str(date.day), str(date.year)]))
        urls.append("".join([url_prefix, date_str, url_suffix]))
    return urls

class DocfestSpider(CrawlSpider):
    name = "dfs"
    allowed_domains = ["prod3.agileticketing.net"]
    dates = fetch_dates()
    start_urls = construct_start_urls(dates)

    def start_requests(self):
        for url in self.start_urls:
            #set a cookie so that the browser doesn't redirect
            yield Request(url, cookies={'ASP.NET_SessionId': 'dnk0o52a5h5x3pff1l5nociv'}, callback=self.parse_screenings)

    def parse_screenings(self, response):
        '''
        Parse http response
        '''
        hxs = HtmlXPathSelector(response)
        no_screenings = hxs.select('//*[@id="ctl00_CPH1_lblNothingToList"]').extract()
        if no_screenings:
            log.msg('No screenings', level=log.INFO)
            return None
        else:
            return self._get_screenings(hxs, response)

    def _get_screenings(self, hxs, response):
        '''
        Parse list of screenings for each date
        '''
        screenings = hxs.select('//div[@class="ItemInfo"]')
        
        for screening in screenings:
            item = DocfestItem()
            self._set_date(item, screening)
            self._set_doc_title(item, screening)
            self._set_venue(item, screening)
            self._set_start_time(item, screening)
            self._set_duration(item, screening)
            self._set_description(item, screening)
            item['info_link'] = response.url
            yield item


    def _set_date(self, item, screening):
        '''
        Parse and format screening date
        '''
        d = screening.select('div[@class="DateTime"]/span[1]/text()').extract()
        dl = self._format_output(d[0]).split('/') if d else None
        # e.g: '6/24/13' => date(2013, 6, 24)
        item['date'] = date(int('20' + dl[2]), int(dl[0]), int(dl[1]))
    

    def _set_doc_title(self, item, screening):
        '''
        Parse and format film title
        '''
        title = screening.select('div[@class="Name"]/text()').extract()
        item['doc_title'] = self._format_output(title[0]) if title else None
    
    def _set_venue(self, item, screening):
        '''
        Parse and format screening location
        '''
        venue = screening.select('div[@class="Venue"]/a/text()').extract()
        item['venue'] = self._format_output(venue[0]) if venue else None 

    def _set_start_time(self, item, screening):
        '''
        Parse and format screening time
        '''
        start_time = screening.select('div[@class="DateTime"]/text()').re('(\d*):00 PM')
        int_start_time = self._format_output(start_time[0]) if start_time else None
        # all of the screenings are in the afternoon, therefore '7 PM' => time(19)
        item['start_time'] = time(12 + int(int_start_time)) 
    
    def _set_duration(self, item, screening):
        '''
        Parse and format the film running time
        '''
        duration = screening.select('div[@class="DateTime"]/span[2]/text()').re('\((\d*) min\)')
        int_duration = self._format_output(duration[0]) if duration else None
        item['duration'] = timedelta(minutes=int(int_duration))

    def _set_description(self, item, screening):
        '''
        Parse and format the film description
        '''
        description_normal = screening.select('div[@class="DescriptionContainer"]/div[1]/text()').extract()
        description_p_tags = screening.select('div[@class="DescriptionContainer"]/div[1]/p/text()').extract()
        # sometimes the description was formatted with p tags
        item['description'] = self._format_output(description_normal[0]) if description_normal else self._format_output(description_p_tags[0]) 
    
    def _format_output(self, unicode_str):
        '''
        Takes a unicode string, and converts it to ascii. Strips trailing and leading whitespace and newlines.
        '''
        ascii_str = unicodedata.normalize('NFKD', unicode_str).encode('ascii','ignore')
        return ascii_str.strip()

    
