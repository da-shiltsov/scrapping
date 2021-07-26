import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

result_outer_links = {}

class LinkSpider(scrapy.Spider):
    name = "mytestcrawler"
    visited_inner_links = set()

    def start_requests(self):
        yield scrapy.Request(url = "http://asperito.ru/1.php", callback = self.parse)

    def parse(self, response):
        inner_link_extractor = LinkExtractor(allow_domains="asperito.ru")
        outer_link_extractor = LinkExtractor(deny_domains="asperito.ru")
        inner_links = inner_link_extractor.extract_links(response)
        outer_links = outer_link_extractor.extract_links(response)

        result_outer_links[response.url] = outer_links

        for link in inner_links:
            if link not in self.visited_inner_links:

        print("------------- inner links:")
        [print(link) for link in inner_links]
        print("------------- outer links:")
        [print(link) for link in outer_links]

    def create_result(self, response)

process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()
