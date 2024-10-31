import logging
import time
from threading import Thread

import schedule


class Updater:

    def __init__(self, data_provider, data_consumer, update_interval):
        self._logger = logging.getLogger(__name__)
        self._data_provider = data_provider
        self._data_consumer = data_consumer
        self._update_interval = update_interval

        self._updater_thread = Thread(target=self._run)
        self._updater_thread.daemon = True

    def start_updating(self):
        schedule.every(self._update_interval).seconds.do(self._update_register)
        self._logger.info('Data updating scheduled to run every %s seconds', self._update_interval)
        self._updater_thread.start()

    def stop_updating(self):
        schedule.clear()
        self._updater_thread.join(0)    # Immediately, there is no graceful shutdown anyway
        self._logger.info('Data updating has stopped')

    def _run(self):
        while True:
            idle_time = schedule.idle_seconds()
            if idle_time > 0:
                time.sleep(idle_time)
            schedule.run_pending()

    def _update_register(self):
        data = self._data_provider.get()
        self._data_consumer.consume(data)
        self._logger.debug('Data updated to %s', data)
