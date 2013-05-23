# Scrapy settings for docfest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'docfest'

SPIDER_MODULES = ['docfest.spiders']
NEWSPIDER_MODULE = 'docfest.spiders'

ITEM_PIPELINES = ['docfest.pipelines.DocfestPipeline']

#I believe that this setting is broken currently. See scrapy project on github. -x
LOG_STDOUT = True

DOWNLOAD_TIMEOUT = 5
# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'mcmguaba (+http://www.mcmguaba.com)'

DF_LOG_FILE = '/var/log/scrapy/docfest.log'
