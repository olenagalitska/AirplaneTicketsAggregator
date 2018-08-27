import scrapy


class WizzNewsSpider(scrapy.Spider):
    name = "uia_news"
    start_urls = [
        'https://www.flyuia.com/ua/en/news/2018'
    ]

    def parse(self, response):
        headings = response.css('div.content div.mt_16 a::text').extract()[:5]
        links = response.css('div.content div.mt_16 h3 a::attr(href)').extract()[:5]
        dates = response.css('div.content div.mt_32 p b::text').extract()[:5]

        news = []

        for i in range(0, len(headings)):
            news.append({"heading": headings[i], "link": "https://www.flyuia.com" + links[i], "date": dates[i], "airline": "UIA"})

        return news
