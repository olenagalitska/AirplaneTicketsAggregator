from app import arangodb


class HistoryManager:
    def insert_history(self, key, search):
        history_collection = arangodb.collection('history')
        search_found = history_collection.get(key)
        if search_found is None:
            history_collection.insert(search)

    def remove_history(self, key, user_id):
        user_activity_collection = arangodb.collection('user_activity')
        # history_flights = arangodb.collection('history')
        user_document = user_activity_collection.get(str(user_id))
        search_ids = user_document['searches']
        for id in search_ids:
            if id == key:
                search_ids.remove(id)
                break
        user_document['searches'] = search_ids
        user_activity_collection.update(user_document)

    def get_history(self, key):
        history_collection = arangodb.collection('history')
        search_found = history_collection.get(key)
        return search_found

