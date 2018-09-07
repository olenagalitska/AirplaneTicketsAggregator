import scrapy
from app import airlines_data_collection
from app import list_of_airlines


class AirlinesInfoSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        super(AirlinesInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.urls_map = dict()
        for airline in list_of_airlines:
            airline_data = airlines_data_collection.get(airline)
            self.start_urls.append((airline_data['links'])['info_link'])
            self.urls_map[(airline_data['links'])['info_link']] = airline

    name = "airlines_info_spider"

    def parse(self, response):

        current_airline = self.urls_map[response.url]

        airline_data = airlines_data_collection.get(current_airline)

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
            if row.css("th::text, th>div::text, th>a::text, th>a.external::text, a[href]::text").extract_first() == 'Website':
                url = row.css('a.external.text::attr(href)').extract_first()
                break

        airline_info_data['founded'] = founded
        airline_info_data['url'] = url

        airline_data['info'] = airline_info_data
        airlines_data_collection.update(airline_data)

        return airline_info_data
