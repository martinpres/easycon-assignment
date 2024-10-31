import json
import logging
import logging.config
import os
import time
from argparse import ArgumentParser

from client import Reader
from client.client_factory import get_modbus_client
from client.data_consumer import DataConsumer
from client.decoder import FloatValueDecoder


def _parse_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)


def _setup_logging(config):
    log_config_path = os.path.join(config.get('log_config'))
    logging.config.fileConfig(log_config_path)


def main():
    argument_parser = ArgumentParser(
        prog='modbus_client',
        description="Periodically reads weather data from server's input registers and stores them to MongoDB"
    )

    argument_parser.add_argument(
        '-c', '--config', required=True, type=str,
        help='configuration JSON file'
    )

    args = argument_parser.parse_args()
    config = _parse_config(args.config)
    _setup_logging(config)

    client = get_modbus_client(config.get('client'))
    data_consumer = DataConsumer(config.get('mongodb'))
    value_decoder = FloatValueDecoder()
    reader = Reader(client, data_consumer, value_decoder, config.get('read_interval'))

    try:
        reader.start_reading()
        while True:
            idle_time = reader.idle_time()
            if idle_time > 0:
                time.sleep(idle_time)
            reader.run_once()
    finally:
        reader.stop_reading()


if __name__ == '__main__':
    main()
