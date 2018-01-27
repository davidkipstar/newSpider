# -*- coding: utf-8 -*-
import scrapy
import spacy
from Newspider.items import ArticleItem

class ArticlespiderSpider(scrapy.Spider):
    name = 'ArticleSpider'
    allowed_domains = ['www.bz-berlin.de']
    start_urls = ['https://www.bz-berlin.de/berlin/reinickendorf/nachbarin-berichtet-so-lief-die-gehweg-geburt-in-reinickendorf']
    def start_request(self,response):
    	urls = ['https://www.bz-berlin.de/berlin/reinickendorf/nachbarin-berichtet-so-lief-die-gehweg-geburt-in-reinickendorf']
    	for url in urls:
    		yield scrapy.Request(url=url,callback=parse,errback = errback_httpbin,dont_filter=True)
    
    def parse(self, response):
        #check if url not included in db or use SCRAPY MIDDLEWARE?!
        article = ArticleItem()
        article['url'] = response.request.url
        #article meta
        artic = response.css('article')[0]
        article['h1'] = artic.xpath('//header/div/h1/text()')
        article['h2'] = artic.xpath('//header/div/h2/text()')
        article_meta = artic.css('header[class="article-meta"]')[0]
        article['author']  = article_meta.xpath('//div/author/span[2]/text()')
        article['bereich'] = article_meta.xpath('//div/div/ul') #iterate? add relation!
        article['refferences'] = article_meta.xpath('//div/div/ul/li/a/@href')
        #TIME FOR DATA

        return article
    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)