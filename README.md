SF Docfest scraper
===============

[SF IndieFest](http://sfindie.com/connect/) holds an annual documentary festival called [Docfest](http://sfindie.com/festivals/sf-docfest/). Unfortunately, the schedule on their website isn't available in any kind of easily exportable format. I wrote this scraper to scrape the film screening schedule and store the data as json.

The data can then be manipulated and imported into a variety of calendar programs, but I structured it specifically for use with the [Google Calendar API](https://gist.github.com/mcmguaba/5640569).

Ultimately this was a quick and dirty project. There is literally no error handling (except for scrapy's default exception handling), and quite a few hacks. The result is a public calendar that can be viewed by adding this to your google calendar:
cmnip8vlkc6gqdtjock584mlug@group.calendar.google.com

Want to run the scraper for yourself? 
1. Generate a valid epguid param in your browser and paste it in [here](https://github.com/mcmguaba/docfest_scraper/blob/master/docfest/spiders/doc_screenings.py#L31). 
2. In that same browser window, inspect your cookie and put that value in [here](https://github.com/mcmguaba/docfest_scraper/blob/master/docfest/spiders/doc_screenings.py#L48).
3. Run the scraper from the command line anywhere inside the scrapy project directory.
```
scrapy crawl dfs
```

Happy scraping!
