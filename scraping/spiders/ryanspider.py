import scrapy


class RyanairNewsSpider(scrapy.Spider):
    name = "ryanair_news"
    start_urls = [
        'https://corporate.ryanair.com/press-releases/'
    ]

    def parse(self, response):
        headings = response.css('div.news-row div.news-excerpt h3 a::text').extract()[:5]
        links = response.css('div.news-row div.news-excerpt h3 a::attr(href)').extract()[:5]
        dates = response.css('div.news-row div.news-excerpt div.news-date::text').extract()[:5]

        news = []

        for i in range(0, len(headings)):
            news.append({"heading": headings[i], "link": links[i], "date": dates[i], "airline": "Ryan Air"})

        return news
