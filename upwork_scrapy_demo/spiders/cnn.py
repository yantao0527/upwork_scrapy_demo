import scrapy


class CnnSpider(scrapy.Spider):
    name = "cnn"
    allowed_domains = ["www.cnn.com"]
    start_urls = ["https://www.cnn.com/"]

    def parse(self, response):
        head_nav = response.css('#header-nav-container')
        world_link = head_nav.xpath('//a[@name="world"]')
        yield from response.follow_all(world_link, callback=self.parse_world)

    def parse_world(self, response):
        middle_east_link = response.xpath('//*[@id="pageHeader"]/div/div/div[1]/div[1]/nav/div/div[8]/a')
        yield from response.follow_all(middle_east_link, callback=self.parse_middle_east)

    def parse_middle_east(self, response):
        articl_links = response.css('div.zone__inner  a.container__link.container_vertical-strip__link')
        # for link in articl_links:
        #     headline = link.css('div.container__headline.container_vertical-strip__headline::text').get()
        #     if headline is not None:
        #         yield {
        #             'title': headline,
        #             'url': link.css('a::attr(href)').get(),
        #         }
        for link in articl_links:
            headline = link.css('div.container__headline.container_vertical-strip__headline::text').get()
            if headline is not None:
                yield response.follow(link.css('a::attr(href)').get(), callback=self.parse_article)

    def parse_article(self, response):
        headline=response.css('div.headline')
        yield {
            'article': headline.css('h1::text').get(),
            'author': headline.css('div.byline__names *::text').extract(),
            'timestamp': headline.css('div.timestamp::text').get(),
            'url': response.url,
        }

