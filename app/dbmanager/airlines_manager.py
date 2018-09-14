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
        airlines = arangodb.collection('airlines_data')
        if airlines.has(airline.lower()):
            airline_data = airlines.get(airline.lower())
            date_parts = date.split('-')
            if len(date_parts) == 3:
                year = "year_" + date_parts[0]
                month = int(date_parts[1])
                stats = airline_data['stats']
                if not year in stats:
                    stats[year] = {"counters": [0] * 12}
                    airline_data['stats'] = stats
                    airlines.update(airline_data)

                year_object = (airline_data['stats'])[year]
                months = year_object['counters']
                months[month - 1] = months[month - 1] + 1
                year_object['counters'] = months
                airlines.update(airline_data)

    def get_airline_stats(self):
        cursor = arangodb.aql.execute('FOR doc IN airlines_data RETURN doc', batch_size=1)
        results = [doc for doc in cursor]
        airline_stats = []
        next_year = datetime.datetime.now().year + 1
        start_year = 2018

        for i in range(start_year, next_year + 1):
            year = "year_" + str(i)
            year_stats = {'year' : i,
                          'airlines' : [],
                          'counters' : []}
            for result in results:
                stats = result['stats']
                if year in stats:
                    year_stats['airlines'].append(result['_key'])
                    year_stats['counters'].append((stats[year])['counters'])
            airline_stats.append(year_stats)

        return airline_stats



