import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

SITE = "https://www.bc-clinic.ru"
SITE_DOMAIN = "bc-clinic.ru"
IGNORED_DOMAINS = ["bc-clinic.ru", "facebook.com", "instagram.com", "vk.com", "wa.me", "google.com", "youtube.com", "medesk.ru"]
LOG_OUTPUT = True
REPORT_FILE = "./bcclinic-outerlinks.txt"

result_outer_links = dict()

class LinkSpider(scrapy.Spider):
    name = "mytestcrawler"
    visited_inner_links = set()

    custom_settings = {
        'LOG_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(url = SITE, callback = self.parse)

    def parse(self, response):
        global result_outer_links

        inner_link_extractor = LinkExtractor(allow_domains=SITE_DOMAIN)
        inner_links = inner_link_extractor.extract_links(response)

        outer_link_extractor = LinkExtractor(deny_domains=IGNORED_DOMAINS)
        outer_links = outer_link_extractor.extract_links(response)

        if len(outer_links) > 0:
            result_outer_links[response.url] = [link.url for link in outer_links]
            if LOG_OUTPUT:
                print("# found in ", response.url , ": ", result_outer_links[response.url])

        for link in inner_links:
            if link not in self.visited_inner_links:
                self.visited_inner_links.add(link)
                yield response.follow(url = link.url, callback = self.parse)


print("start scanning ...")
process = CrawlerProcess()
process.crawl(LinkSpider)
process.start()

with open(REPORT_FILE,"w+") as fp:
    fp.write(f"Outer links for domain {SITE}\n")
    fp.write( "--------------------------------------------------------------------------------------------------\n\n")
    for link, outer_links in result_outer_links.items():
        fp.write("\n" + link + "\n")
        for outer_link in outer_links:
            fp.write("\t" + outer_link + "\n")

print("done")
