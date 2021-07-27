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
        global result_outer_links
        print("# parse call: ", response.url)

        inner_link_extractor = LinkExtractor(allow_domains="asperito.ru")
        inner_links = inner_link_extractor.extract_links(response)

        outer_link_extractor = LinkExtractor(deny_domains="asperito.ru")
        outer_links = outer_link_extractor.extract_links(response)

        result_outer_links[response.url] = outer_links
        print("# outer links:", outer_links)

        for link in inner_links:
            if link not in self.visited_inner_links:
                self.visited_inner_links.append(link)
                print("# link: ", link)
                yield response.follow(url = link, callback = self.parse)


print("поехали")
process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()
