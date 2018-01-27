import scrapy
import datetime
import time

from Newspider.items import SnapshotItem
from Newspider.items import ArticleItem
from scrapy.http import Request


class pagespider(scrapy.Spider):
    #
    name = 'pagespider'
    #
    def start_request(self):
        urls = ['http://www.bz-berlin.de/',
        'https://www.bz-berlin.de/berlin-sport']
        for url in urls:
            yield Request(url=url,callback=self.parse_page)
        article_urls = ['https://www.bz-berlin.de/tatort/menschen-vor-gericht/er-nahm-tausende-euro-mit-die-ein-rentner-im-geldautomaten-liess']
        for url in article_urls:
            yield Request(url=url,callback=self.parse_article)

    def parse_article(self,response):
        #check if url not included in db or use SCRAPY MIDDLEWARE?!
        article = ArticleItem()
        article['url'] = response.request.url

        if(response.meta):
            #'invoked'
            article['timestamp'] = response.meta['timestamp']
            article['body'] = response.meta['body']
        else:
            #'calling without callback invoke'
            print('no initial url')

        artic = response.css('article')[0]
        article['h1'] = artic.xpath('header/div/h1/text()')
        article['h2'] = artic.xpath('header/div/h2/text()')

        article_meta = artic.css('header[class="article-meta"]')[0]


        article['author'] = article_meta.xpath('div/author/span[2]/text()')
        
        #TIME FOR DATA

        #article['bereich']= article_meta.xpath()
        #article['aktualisiert']
        #article['thema']
        #article['bow'] = 
        return article
    def parse_page(self,response):
        #
        page = SnapshotItem()
        page['url'] = response.url       
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        page['timestamp'] = st
        yield page
        sections = response.css('div[class="row"]')
        print('hellooo')
        for idx,block in enumerate(sections):
            articles = block.xpath('.//div/div')
            for idy,article in enumerate(articles):
                href = article.xpath('a/@href').extract_first()
                print('url:',href)
                request = scrapy.Request(url=href,callback = self.parse_article)
                request.meta['rank'] = str(idx) + '-' +str(idy)
                request.meta['timestamp'] = st
                request.meta['body'] = article.extract()
                yield request
