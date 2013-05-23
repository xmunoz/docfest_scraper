import logging
from scrapy.log import ScrapyFileLogObserver
from scrapy.conf import settings

logfile = open(settings['DF_LOG_FILE'], 'w')
log_observer = ScrapyFileLogObserver(logfile, level=logging.WARNING)
log_observer.start()

