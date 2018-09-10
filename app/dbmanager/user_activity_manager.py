from app import arangodb
from app.models import Flight

class UserActivityManager:
    def init_user(self, user_id):
        user_activity = arangodb.collection('user_activity')
        activity = {'_key': str(user_id), 'flights': [], 'searches': []}
        user_activity.insert(activity)


    def insert_flight(self, flight_id, user_id):
        user_activity = arangodb.collection('user_activity')
        activity = user_activity.get(str(user_id))
        list_of_flights = activity['flights']
        list_of_flights.append(flight_id)
        activity['flights'] = list_of_flights
        user_activity.update(activity)


    def insert_search(self, key, user_id):
        user_activity = arangodb.collection('user_activity')
        user_document = user_activity.get(str(user_id))
        list_of_searches = user_document['searches']
        already_in_history = False

        # check if already in user's history
        for user_search in list_of_searches:
            if user_search == key:
                already_in_history = True
                break
        if not already_in_history:
            list_of_searches.append(key)
            user_document['searches'] = list_of_searches
            user_activity.update(user_document)


    def get_user_history(self, user_id):
        user_activity = arangodb.collection('user_activity')
        history_flights = arangodb.collection('history')
        user_document = user_activity.get(str(user_id))
        search_ids = user_document['searches']
        list_of_searches = []
        for id in search_ids:
            search = history_flights.get(id)
            list_of_searches.append(search)
        return list_of_searches

    def get_saved_flights(self, user_id):
        user_activity = arangodb.collection('user_activity')
        user_document = user_activity.get(str(user_id))
        flights_ids = user_document['flights']
        list_of_flights = []
        for id in flights_ids:
            flight = Flight.query.filter_by(id=id).first()
            list_of_flights.append(flight)
        return list_of_flights
