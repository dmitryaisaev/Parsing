import scrapy
from scrapy.http import HtmlResponse
from parsing_job.items import ParsingJobItem

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?area=1&search_field=name&search_field=company_name&search_field=description&text=Delphi&ored_clusters=true&enable_snippets=true'
        ]

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        vac_links = response.xpath('//a[@data-qa="serp-item__title"]/@href').getall()
        for link in vac_links:
            yield response.follow(link, callback=self.parse_vac)
        
        
    def parse_vac(self, response:HtmlResponse):
        vac_name = response.css('h1::text').get()
        vac_url = response.url
        vac_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        
        
        yield ParsingJobItem(
                name = vac_name, 
                url = vac_url, 
                salary = vac_salary
        )