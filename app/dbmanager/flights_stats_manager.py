from app import arangodb


class FlightsStatsManager:

    @staticmethod
    def get_current_stats_for(flight_id):
        flights_stats_collection = arangodb.collection('flights_stats')
        document = flights_stats_collection.get(str(flight_id))
        n = len(document['prices'])
        return (document['prices'])[n-1]

    @staticmethod
    def get_all_stats_for(flight_id):
        flights_stats_collection = arangodb.collection('flights_stats')
        document = flights_stats_collection.get(str(flight_id))
        return document['prices']

    @staticmethod
    def update_stats(flight_id, updated_fares):
        flights_stats_collection = arangodb.collection('flights_stats')
        document = flights_stats_collection.get(str(flight_id))
        prices = document['prices']
        prices.append(updated_fares)
        document['prices'] = prices
        flights_stats_collection.update(document)
