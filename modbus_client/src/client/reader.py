import logging

import schedule

from client.model.weather_info import WeatherInfo


class Reader:

    def __init__(self, client, data_consumer, value_decoder, read_interval):
        self._logger = logging.getLogger(__name__)
        self._client = client
        self._data_consumer = data_consumer
        self._value_decoder = value_decoder
        self._read_interval = read_interval

    def start_reading(self):
        if not self._client.connect():
            self._logger.error('Unable to connect to the Modbus server')
        else:
            self._logger.info('Client connected to the Modbus server')

        self._schedule_job()

    def stop_reading(self):
        self._client.close()
        self._logger.info('Client disconnected')

    def run_once(self):
        schedule.run_pending()

    def idle_time(self):
        return schedule.idle_seconds()

    def _schedule_job(self):
        schedule.every(self._read_interval).seconds.do(self._read_from_server)
        self._logger.info('Reading scheduled to run every %s seconds', self._read_interval)

    def _read_from_server(self):
        result = self._client.read_input_registers(0x0, 6)
        if result.isError():
            self._logger.error('Failed to read from the register: %s', result)
        else:
            registers = result.registers
            self._logger.debug('Client successfully read register values %s', registers)

            self._data_consumer.consume(WeatherInfo.from_list(self._value_decoder.decode(registers)))
