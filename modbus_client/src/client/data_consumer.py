import logging

import pymongo

from client.model.weather_info import WeatherInfo


class DataConsumer:

    def __init__(self, mongo_config):
        self._logger = logging.getLogger(__name__)

        self._mongo_client = pymongo.MongoClient(mongo_config.get('connection'))
        self._mongo_db = self._mongo_client[mongo_config.get('database')]
        self._mongo_collection = self._mongo_db[mongo_config.get('collection')]

        self._logger.info('MongoDB connected')

    def consume(self, weather_info: WeatherInfo):
        mongo_insert_result = self._mongo_collection.insert_one(weather_info.to_dict())
        self._logger.debug('Data stored with id %s', str(mongo_insert_result.inserted_id))

    def close(self):
        self._mongo_client.close()
        self._logger.info('Connection to MongoDB closed')
