import logging

import pymongo
from psycopg_pool import ConnectionPool

from .model.message import Message


class DataConsumer:

    def __init__(self, mongo_config, postgres_config):
        self._logger = logging.getLogger(__name__)

        self._mongo_client = pymongo.MongoClient(mongo_config.get('connection'))
        self._mongo_db = self._mongo_client[mongo_config.get('database')]
        self._mongo_collection = self._mongo_db[mongo_config.get('collection')]

        self._logger.info('MongoDB connected')

        pool_size = postgres_config.get('pool')
        self._postgres_connection_pool = ConnectionPool(
            conninfo=postgres_config.get('connection'),
            min_size=pool_size.get('min_size'),
            max_size=pool_size.get('max_size')
        )

        self._logger.info('PostgreSQL connected')

    def consume(self, message: Message):
        mongo_insert_result = self._mongo_collection.insert_one(message.to_dict())
        try:
            with self._postgres_connection_pool.connection() as postgres_connection:
                with postgres_connection.cursor() as postgres_cursor:
                    postgres_cursor.execute(
                        'INSERT INTO record_metadata (topic, mongo_id) VALUES (%s, %s)',
                        (message.topic, str(mongo_insert_result.inserted_id))
                    )
        except Exception as e:
            self._mongo_collection.delete_one({"_id": mongo_insert_result.inserted_id})
            self._logger.error('Transaction failed and was rolled back: %s', e)

    def close(self):
        self._mongo_client.close()
        self._logger.info('Connection to MongoDB closed')

        self._postgres_connection_pool.close()
        self._logger.info('Connection to PostgreSQL closed')
