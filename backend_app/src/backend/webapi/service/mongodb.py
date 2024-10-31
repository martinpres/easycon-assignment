import atexit

import pymongo


class MongoDbService:

    def __init__(self, mongo_config):
        self._client = pymongo.MongoClient(mongo_config.get('connection'))
        self._database = self._client[mongo_config.get('database')]
        atexit.register(self._client.close)

    def list_collection_content(self, collection_name):
        return list(self._database[collection_name].find({}, {"_id": 0}))
