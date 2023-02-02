import scrapy
from scrapy.http import HtmlResponse
from parsing_job.items import AdsParserItem
from scrapy.loader import ItemLoader

class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']
        self.start_urls = ['https://www.castorama.ru/catalogsearch/result/?q=паяльник']
        print(f'\n##############\n{self.start_urls}\n##############\n')

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AdsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', '//div[@class="add-to-cart__price js-fixed-panel-trigger"]//div[@class="price-wrapper _with-discount "]//div[@class="current-price"]//div[@class="price-box"]//span[@class="price"]/span/span[1]/text()')
        loader.add_xpath('photos', '//img[@class="zoomImg"]/@src')
        loader.add_value('url', response.url)
        yield loader.load_item()


