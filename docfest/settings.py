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

#disable 302s
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': None,
}

LOG_STDOUT = True

DOWNLOAD_TIMEOUT = 5

USER_AGENT = 'mcmguaba (+http://www.mcmguaba.com)'

DF_LOG_FILE = '/var/log/scrapy/docfest.log'
