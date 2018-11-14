import scrapy

import logging.config

import yaml

from arango import ArangoClient


class AirlinesInfoSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        super(AirlinesInfoSpider, self).__init__(*args, **kwargs)

        with open('../app/conf/logging.yml', 'r') as stream:
            logging_config = yaml.load(stream)
        logging.config.dictConfig(logging_config)

        self.custom_logger = logging.getLogger('logger')

        self.custom_logger.info('airlines info scraper logger started')

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
            self.start_urls.append((airline_data['links'])['info_link'])
            self.urls_map[(airline_data['links'])['info_link']] = airline

        self.custom_logger.info('list of airlines: ')
        for airline in self.list_of_airlines:
            self.custom_logger.info(str(airline))

        self.custom_logger.info('start urls:')
        for url in self.start_urls:
            self.custom_logger.info(str(url))
        self.custom_logger.info('end of init')

    name = "airlines_info_spider"

    def parse(self, response):
        print("\n\n\ntest\n\n\n")

        self.custom_logger.info('scraping url: ' + str(response.url))

        current_airline = self.urls_map[response.url]

        self.custom_logger.info('current_airline: ' + str(current_airline))

        airline_data = self.airlines_data_collection.get(current_airline)

        if 'info' not in airline_data:
            airline_data['info'] = {}

        airline_info_data = airline_data['info']

        table = response.css("table.infobox.vcard")[0]
        caption = table.css("caption::text").extract_first()
        codes = table.css(".nickname::text")

        if len(codes) == 4:
            del codes[1]

        airline_info_data['caption'] = str(caption).replace('\n', '')
        airline_info_data['iata'] = str(codes[0].extract()).replace('\n', '')
        airline_info_data['icao'] = str(codes[1].extract()).replace('\n', '')
        airline_info_data['callsign'] = str(codes[2].extract()).replace('\n', '')

        info = table.css("tbody>tr")
        info = info[4:]

        founded = str(info[0].css("td::text, td>div::text, td>a::text").extract_first()).replace('\n', '')

        for row in info:
            if row.css(
                    "th::text, th>div::text, th>a::text, th>a.external::text, a[href]::text").extract_first() == 'Website':
                url = row.css('a.external.text::attr(href)').extract_first()
                break

        airline_info_data['founded'] = founded
        airline_info_data['url'] = url

        airline_data['info'] = airline_info_data
        self.airlines_data_collection.update(airline_data)

        return airline_info_data
