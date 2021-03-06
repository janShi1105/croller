import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from my_project.items import MyProjectItem


class QuotesSpider(CrawlSpider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    rules = (
        Rule(
            LinkExtractor(allow=r'.*'),
            callback='parse_start_url',
            follow=True,
        ),
    )

    def parse_start_url(self, response):
        return self.parse_item(response)

    def parse_item(self, response):
        items = []
        for i, quote_html in enumerate(response.css('div.quote')):
            if i > 1:
                return items
            item = MyProjectItem()
            item['author'] = quote_html.css('small.author::text').extract_first()
            item['text'] = quote_html.css('span.text::text').extract_first()
            item['tags'] = quote_html.css('div.tags a.tag::text').extract()
            items.append(item)

