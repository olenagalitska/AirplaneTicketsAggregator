from app import arangodb


class SavedFlightsManager:
    def init_flight(self, flight_id, user_id):
        saved_flights_collection = arangodb.collection('saved_flights')
        if not saved_flights_collection.has(str(flight_id)):
            # first user who saved the flight
            flight = {"_key": str(flight_id), 'flight_id': [flight_id], "users": [user_id]}
            saved_flights_collection.insert(flight)
