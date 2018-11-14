import scrapy
import json


class AirBalticSpider(scrapy.Spider):

    def __init__(self, depart, arrival, adults, children, infants, date):
        self.arrival = arrival
        self.depart = depart
        self.adults = adults
        self.children = children
        self.infants = infants
        self.date = date

    name = "airBaltic"

    def start_requests(self):
        urls = ["https://tickets.airbaltic.com/en/book/avail"]
        data = {"action2": "avail", "width": '1301', "heights": "672", "p": "bti", "pos": "ZZ", "l": "en",
                "traveltype": "bti", "origin": self.depart, "origin_type": "A", "destin": self.arrival,
                "destin_type": "A", "numadt": self.adults, "numchd": self.children, "numinf": self.infants,
                "bbv": '0', "sref": '', "legs": '1',
                "flt_leaving_on": self.date}
        for url in urls:
            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

    def parse(self, response):
        classes = ['EC', 'ER', 'BR']
        times = response.css('div.time')
        print("----------in parse")
        print(response.body)
        flights = {
            "size": len(times),
            "flights": []
        }
        counter = 0
        for time in times:
            flight_time = time.css('::text').extract_first()
            fares = []
            for one_class in classes:
                price = response.css('#id_fare_' + one_class + '_0_0')
                full = price.css('::text').extract_first()
                cents = price.css('span.cents::text').extract_first()
                full_price = float(full) + (float(cents) / 100)
                fares.append(full_price)

            json_flight = {
                "airportA": self.depart,
                "airportB": self.arrival,
                "airline": "airBaltic",
                "dateDeparture": self.date,
                "dateArrival": '',
                "timeDeparture": (flight_time.split(' - ')[0]).replace(" ", ""),
                "timeArrival": (flight_time.split(' - ')[1]).replace(" ", ""),
                "number": 'airbaltic' + self.date + self.depart + self.arrival + str(counter),
                "types": ['Basic', 'Premium', 'Business'],
                "fares": fares,
                "url": "https://www.airbaltic.com/en-ZZ/index"
            }
            (flights["flights"]).append(json_flight)
            counter = + 1
        print(flights)
        with open(self.depart + self.arrival + self.date + self.adults + self.children + self.infants + '.json',
                  'w') as outfile:
            outfile.write(json.dumps(flights))

        # for i in range(0)
