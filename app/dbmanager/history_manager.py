from app import arangodb

class HistoryManager:
    def insert_history(self, key, search):
        history = arangodb.collection('history')
        search_found = history.get(key)
        if search_found is None:
            history.insert(search)

    def remove_history(self, key, user_id):
        user_activity = arangodb.collection('user_activity')
        # history_flights = arangodb.collection('history')
        user_document = user_activity.get(str(user_id))
        search_ids = user_document['searches']
        for id in search_ids:
            if id == key:
                search_ids.remove(id)
                break;
        user_document['searches'] = search_ids
        user_activity.update(user_document)