import scrapy

import urllib.parse

import logging.config

import yaml

from arango import ArangoClient


class AirlinesNewsSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        super(AirlinesNewsSpider, self).__init__(*args, **kwargs)

        with open('../app/conf/logging.yml', 'r') as stream:
            logging_config = yaml.load(stream)
        logging.config.dictConfig(logging_config)

        self.custom_logger = logging.getLogger('logger')

        self.custom_logger.info('airlines news scraper logger started')

        # python-arango

        # Initialize the client for ArangoDB.
        # logger.info('try to init ArangoClient(...)')
        arangodb_client = ArangoClient(protocol='http', host='localhost', port=8529)
        # logger.info('succeeded')

        # logger.info('try to connect to arango _system')
        sys_db = arangodb_client.db('_system', username='root', password='')
        # logger.info('succeeded')

        if not sys_db.has_database('whatafly'):
            # logger.info('_system does not have whatafly db. try to create it')
            sys_db.create_database('whatafly')
            # logger.info('succeeded')

        # logger.info('try to connect to whatafly')
        arangodb = arangodb_client.db('whatafly', username='arango_user', password='mkh8JTbE793kNtXr')
        # logger.info('succeeded')

        # logger.info('try to get airlines_data collection from whatafly')
        self.airlines_data_collection = arangodb.collection('airlines_data')
        # logger.info('succeeded')

        self.list_of_airlines = []

        cursor_list_of_airlines = self.airlines_data_collection.keys()

        for airline in cursor_list_of_airlines:
            self.list_of_airlines.append(airline)

        self.start_urls = []
        self.urls_map = dict()

        for airline in self.list_of_airlines:
            airline_data = self.airlines_data_collection.get(airline)
            self.start_urls.append((airline_data['links'])['news_link'])
            self.urls_map[(airline_data['links'])['news_link']] = airline

        self.custom_logger.info('list of airlines: ')
        for airline in self.list_of_airlines:
            self.custom_logger.info(str(airline))

        self.custom_logger.info('start urls:')
        for url in self.start_urls:
            self.custom_logger.info(str(url))
        self.custom_logger.info('end of init')

    name = "airlines_news_spider"

    def parse(self, response):

        self.custom_logger.info('scraping url: ' + str(response.url))

        current_airline = self.urls_map[response.url]

        self.custom_logger.info('current_airline: ' + str(current_airline))

        airline_data = self.airlines_data_collection.get(current_airline)
        airline_news_data = airline_data['news_data']

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

        if 'news' not in airline_news_data:
            airline_news_data['news'] = {}
            latest_version = 0
        else:
            latest_version = int(airline_news_data['latest_version']) + 1

        (airline_news_data['news'])['v.' + str(latest_version)] = updated_news

        airline_data['news_data'] = airline_news_data
        self.airlines_data_collection.update(airline_data)

        airline_data = self.airlines_data_collection.get(current_airline)
        (airline_data['news_data'])['latest_version'] = str(latest_version)
        self.airlines_data_collection.update(airline_data)

        return updated_news
