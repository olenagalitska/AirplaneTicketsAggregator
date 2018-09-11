from app import arangodb, list_of_airlines
import datetime


class AirlinesManager:
    def create_stats_fields(self):
        airlines_data_collection = arangodb.collection('airlines_data')
        curr_year = datetime.datetime.now().year
        next_year = curr_year + 1
        curr_year = 'year_' + str(curr_year)
        next_year = 'year_' + str(next_year)

        for airline in list_of_airlines:
            airline_data = airlines_data_collection.get(airline)

            if 'stats' not in airline_data:
                airline_data['stats'] = {}
                stats = airline_data['stats']
                stats[curr_year] = {"counters": [0] * 12}
                stats[next_year] = {"counters": [0] * 12}
            else:
                stats = airline_data['stats']
                if curr_year not in stats:
                    stats[curr_year] = {"counters": [0] * 12}

                if next_year not in stats:
                    stats[next_year] = {"counters": [0] * 12}

            airline_data['stats'] = stats
            airlines_data_collection.update(airline_data)

    def increase_count(self, airline, date):
        print("in increase")
        print(date)
        airlines_data_collection = arangodb.collection('airlines_data')
        if airlines_data_collection.has(airline.lower()):
            airline_data = airlines_data_collection.get(airline.lower())
            date_parts = date.split('-')

            year = "year_" + date_parts[0]
            month = int(date_parts[1])
            stats = airline_data['stats']
            year_object = stats[year]
            months = year_object['counters']
            months[month - 1] = months[month - 1] + 1
            year_object['counters'] = months
            airline_data['stats'][year] = year_object
            airlines_data_collection.update(airline_data)
