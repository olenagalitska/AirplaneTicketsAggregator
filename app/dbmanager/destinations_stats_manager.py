import datetime

from app import arangodb
from app.models import Airport


class DestinationsStatsManager:
    def create_stats_fields(self):
        destinations_stats_collection = arangodb.collection('destinations_stats')
        airports = Airport.query.order_by("country").all()

        curr_year = datetime.datetime.now().year
        next_year = curr_year + 1
        curr_year = 'year_' + str(curr_year)
        next_year = 'year_' + str(next_year)

        counters = {"counters": [0] * 12}

        city = {curr_year: counters, next_year: counters}

        for airport in airports:
            if not destinations_stats_collection.has(str(airport.country)):

                country = {'_key': str(airport.country), str(airport.city): city}
                destinations_stats_collection.insert(country)
            else:
                country = destinations_stats_collection.get(str(airport.country))
                if str(airport.city) not in country:
                    country[str(airport.city)] = city
                    destinations_stats_collection.update(country)

    def increase_counter(self, airport, date):
        destinations_stats_collection = arangodb.collection('destinations_stats')

        # TODO: check in psql if there is such airport
        airports = Airport.query.order_by("country").all()
        if airport in airports:
            if airport.country in destinations_stats_collection:
                country = destinations_stats_collection.get(str(airport.country))
                if airport.city in country:
                    city = country[str(airport.city)]
                    date_parts = date.split('-')
                    year = "year_" + date_parts[0]
                    month = int(date_parts[1])
                    if year in city:
                        year_object = city[year]

                        months = year_object['counters']
                        months[month - 1] += 1
                        year_object['counters'] = months
                        city[year] = year_object
                        country[str(airport.city)] = city
                        destinations_stats_collection.update(country)
