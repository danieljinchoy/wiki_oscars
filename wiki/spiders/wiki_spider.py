# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from wiki.items import WikiItem


class WikiSpider(Spider):
    name = 'wiki_spider'
    allowed_urls = ['https://en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/w/index.php?title=List_of_Academy_Award-winning_films&diff=968702539&oldid=961298911']

    def parse(self, response):
        # Find all the table rows
        rows = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr')[1:]
        
        # The movie title could be of different styles so we need to provide all the possibilities.
        for row in rows:

            film = ''.join(row.xpath('./td[1]//text()').extract())
            # film = row.xpath('./td[1]//text()').extract_first()

            # Relative xpath for all the other columns
            year = int(row.xpath('./td[2]/a/text()').extract_first())
            awards = row.xpath('./td[3]/text()').extract_first()
            nominations = row.xpath('./td[4]/text()').extract_first().strip()
            is_bestpicture = bool(row.xpath('./@style'))

            # Initialize a new WikiItem instance for each movie.
            item = WikiItem()
            item['film'] = film
            item['year'] = year
            item['awards'] = awards
            item['nominations'] = nominations
            item['is_bestpicture'] = is_bestpicture

            yield item