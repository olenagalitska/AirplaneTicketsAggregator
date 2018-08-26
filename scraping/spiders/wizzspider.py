import scrapy


class WizzNewsSpider(scrapy.Spider):
    name = "wizzair_news"
    start_urls = [
        'https://wizzair.com/en-gb/information-and-services/about-us/news/#/'
    ]

    def parse(self, response):
        headings = response.css('li.article-list__result h3::text').extract()[:10]
        links = response.css('li.article-list__result a::attr(href)').extract()[:10]
        dates = response.css('li.article-list__result p::text').extract()[:10]

        news = []

        for i in range(0, len(headings)):
            news.append({"heading": headings[i], "link": links[i], "date": dates[i], "airline": "Wizz Air"})


        return news


