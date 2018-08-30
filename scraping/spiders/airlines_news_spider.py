import scrapy
from app import airlines_data_collection
from app import list_of_airlines
import urllib.parse


class AirlinesNewsSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        super(AirlinesNewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        for airline in list_of_airlines:
            airline_data = airlines_data_collection.get(airline)
            self.start_urls.append((airline_data['links'])['news_link'])

    name = "airlines_news_spider"

    def parse(self, response):

        current_airline = ''

        for i in range(len(list_of_airlines)):
            if list_of_airlines[i] in response.url:
                current_airline = list_of_airlines[i]
                break

        airline_data = airlines_data_collection.get(current_airline)

        airline_news_data = airline_data['news']

        css_headings = (airline_news_data['selectors'])['css_headings']

        css_links = (airline_news_data['selectors'])['css_links']

        css_dates = (airline_news_data['selectors'])['css_dates']

        headings = response.css(css_headings).extract()[:5]
        links = response.css(css_links).extract()[:5]
        dates = response.css(css_dates).extract()[:5]

        updated_news = []

        for i in range(0, len(headings)):
            updated_news.append(
                {"heading": headings[i], "link": str(urllib.parse.urljoin(response.url, links[i])), "date": dates[i]}
            )

        latest_version = int(airline_news_data['latest_version'])
        latest_version += 1

        airline_news_data['v.' + str(latest_version)] = updated_news

        airline_data['news'] = airline_news_data
        airlines_data_collection.update(airline_data)

        # airlines_data_collection.update(airline_data)  # not sure if that will update what i mean

        airline_data = airlines_data_collection.get(current_airline)
        (airline_data['news'])['latest_version'] = str(latest_version)
        airlines_data_collection.update(airline_data)

        return updated_news
