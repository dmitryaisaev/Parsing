import scrapy
from scrapy.http import HtmlResponse
from parsing_job.items import AdsParserItem
from scrapy.loader import ItemLoader

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//div[@class='phytpj4_plp largeCard']/a")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AdsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//showcase-price-view[@slot='primary-price'")
        loader.add_xpath('photos', "//img[@class='pyak1c8_pdp']/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()


