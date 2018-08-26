import scrapy


class WizzNewsSpider(scrapy.Spider):
    name = "wizz_news"
    start_urls = [
        'https://wizzair.com/en-gb/information-and-services/about-us/news/#/'
        # 'https://corporate.ryanair.com/press-releases/'
    ]

    def parse(self, response):
        headings = response.css('li.article-list__result h3::text').extract()[:10]
        links = response.css('li.article-list__result a::attr(href)').extract()[:10]
        dates = response.css('li.article-list__result p::text').extract()[:10]


        result = """
        <hr>
        """

        for i in range(0, len(headings)):
            result += "<p>" + headings[i] + "</p>"
            result += "<a href=" + links[i] + ">Read more...</a>"
            result += "<p>" + dates[i] + "</p> <hr>"

        print(result)

        filename = '../../../app/templates/wizz_news.html'
        with open(filename, 'a') as f:
            f.write(result)
