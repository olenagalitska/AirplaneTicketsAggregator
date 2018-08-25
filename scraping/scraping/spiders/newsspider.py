import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        'https://wizzair.com/en-gb/information-and-services/about-us/news/#/'
        # 'https://corporate.ryanair.com/press-releases/',
        # 'https://www.flyuia.com/ua/en/news/2018',
    ]

    def parse(self, response):
        l = response.css(".article-list")[0]
        result = """
        <h1>it works</h1>
        """

        filename = '../../../app/templates/news.html'
        with open(filename, 'a') as f:
            f.write(result)
