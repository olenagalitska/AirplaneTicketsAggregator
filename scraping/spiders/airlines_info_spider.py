import scrapy
from app import airlines_data_collection
from app import list_of_airlines


class AirlinesInfoSpider(scrapy.Spider):

    def __init__(self, category=None, *args, **kwargs):
        super(AirlinesInfoSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        for airline in list_of_airlines:
            airline_data = airlines_data_collection.get(airline)
            self.start_urls.append((airline_data['links'])['info_link'])

    name = "airlines_info_spider"

    def parse(self, response):

        result = {}

        table = response.css("table.infobox.vcard")[0]
        caption = table.css("caption::text").extract_first()
        codes = table.css(".nickname::text")

        if len(codes) == 4:
            del codes[1]

        result['caption'] = caption
        result['iata'] = codes[0].extract()
        result['icao'] = codes[1].extract()
        result['callsign'] = codes[2].extract()

        info = table.css("tbody>tr")
        info = info[4:]

        founded = info[0].css("td::text, td>div::text, td>a::text").extract_first()

        result['founded'] = founded

