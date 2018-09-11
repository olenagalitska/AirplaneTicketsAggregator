from app import arangodb


class AirlinesManager:
    def increase_count(self, airline, date):
        print("in increase")
        print(date)
        airlines_data = arangodb.collection('airlines_data')
        if airlines_data.has(airline.lower()):
            airline_data = airlines_data.get(airline.lower())
            date_parts = date.split('-')

            year = "year_" + date_parts[0]
            month = int(date_parts[1])
            stats = airline_data['stats']
            try:
                year_object = stats[year]
            except Exception:
                stats[year] = {"counters": [0] * 12}
                airline_data['stats'] = stats
                airlines_data.update(airline_data)
                airline_data = airlines_data.get(airline.lower())
                year_object = stats[year]
            months = year_object['counters']
            months[month - 1] = months[month - 1] + 1
            year_object['counters'] = months
            airline_data['stats'][year] = year_object
            airlines_data.update(airline_data)
