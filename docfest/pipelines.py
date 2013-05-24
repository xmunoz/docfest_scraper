#!/usr/bin/env python

from scrapy import log
from pprint import pformat
import json
from datetime import datetime, date, time

class DocfestPipeline(object):
    def __init__(self):
        '''
        Write data to file
        '''
        self.f = open('../../dumped_screenings.json', 'w')
        self.all_items = []
        
    def process_item(self, item, spider):
        '''
        Created a list with all of the screening dicts
        ''' 
        # expected datetime format
        datetime_format = "%Y-%m-%dT%H:%M:%S-07:00"
        
        start_datetime = datetime.combine(item['date'], item['start_time'])
        start_datetime_formatted = start_datetime.strftime(datetime_format)
        
        #compute end time from start time and duration
        end_datetime = start_datetime + item['duration']
        end_datetime_formatted = end_datetime.strftime(datetime_format)
       
        #format for use with google calendar api -- post events endpoint
        self.all_items.append({
            "end": {"dateTime": end_datetime_formatted},
            "start": {"dateTime": start_datetime_formatted},
            "summary": item['doc_title'],
            "description": item['description'] + '\\n' + item['info_link'],
            "location": item['venue'],
        })
        return item

    def close_spider(self, spider):
        '''
        Dump json to file
        '''
        #dump list to file as json
        json.dump(self.all_items, self.f)
        self.f.close()

