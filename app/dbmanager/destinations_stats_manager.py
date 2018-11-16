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
            country_key = str(airport.country).replace(' ', '_')
            if not destinations_stats_collection.has(country_key):

                country = {'_key': country_key, str(airport.city): city}
                destinations_stats_collection.insert(country)
            else:
                country = destinations_stats_collection.get(country_key)
                if str(airport.city) not in country:
                    country[str(airport.city)] = city
                    destinations_stats_collection.update(country)

    def increase_counter(self, airport, date):
        destinations_stats_collection = arangodb.collection('destinations_stats')

        # TODO: check in psql if there is such airport
        airports = Airport.query.order_by("country").all()
        if airport in airports:
            country_key = str(airport.country).replace(' ', '_')
            print(country_key)

            if country_key in destinations_stats_collection:
                country = destinations_stats_collection.get(country_key)
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

    def get_destinations_stats(self, year, month):
        cursor = arangodb.aql.execute('FOR doc IN destinations_stats RETURN doc', batch_size=1)
        results = [doc for doc in cursor]
        destinations_stats = []

        year = "year_" + str(year)
        month = int(month)

        for result in results:
            for maybe_city in result.keys():
                if maybe_city[0] != '_':

                    if month != 0:
                        print('here')
                        stats_object = {'country': result['_key'],
                                        'city': maybe_city,
                                        'amount': result[maybe_city][year]['counters'][month - 1]}
                    else:
                        print(sum(result[maybe_city][year]['counters']))
                        stats_object = {'country': result['_key'],
                                        'city': maybe_city,
                                        'amount': sum(result[maybe_city][year]['counters'])}
                    destinations_stats.append(stats_object)
        print('res', destinations_stats)
        return destinations_stats
