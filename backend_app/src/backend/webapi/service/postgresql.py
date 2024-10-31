import atexit

from psycopg_pool import ConnectionPool

from backend.webapi.model.record_metadata import RecordMetadata


class PostgresqlService:

    def __init__(self, postgres_config):
        self._config = postgres_config
        self._table = self._config.get('table')
        self._postgres_connection_pool = None

    def list_metadata(self):
        if self._postgres_connection_pool is None:
            # Connects lazily
            self._connect()

        with self._postgres_connection_pool.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM record_metadata')
                rows = cursor.fetchall()

                return [RecordMetadata.from_tuple(row).to_dict() for row in rows]

    def _connect(self):
        pool_size = self._config.get('pool')
        self._postgres_connection_pool = ConnectionPool(
            conninfo=self._config.get('connection'),
            min_size=pool_size.get('min_size'),
            max_size=pool_size.get('max_size')
        )

        atexit.register(self._postgres_connection_pool.close)
