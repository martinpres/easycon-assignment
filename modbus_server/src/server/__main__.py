import json
import logging
import logging.config
import os
from argparse import ArgumentParser

from server import Server
from server.context_factory import get_context
from server.data_consumer import DataConsumer
from server.encoder import FloatValueEncoder
from server.updater import Updater
from server.weather_data_provider import DataProvider


def _parse_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)


def _setup_logging(config):
    log_config_path = os.path.join(config.get('log_config'))
    logging.config.fileConfig(log_config_path)


def main():
    argument_parser = ArgumentParser(
        prog='modbus_server',
        description='Periodically reads weather data from public WEB API and stores it in input registers.'
    )

    argument_parser.add_argument(
        '-c', '--config', required=True, type=str,
        help='configuration JSON file'
    )

    args = argument_parser.parse_args()
    config = _parse_config(args.config)
    _setup_logging(config)

    context = get_context()
    server = Server(context, config.get('server'))

    data_provider = DataProvider(config.get('data_source'))
    value_encoder = FloatValueEncoder()
    data_consumer = DataConsumer(context, value_encoder)
    updater = Updater(data_provider, data_consumer, config.get('update_interval'))

    try:
        updater.start_updating()
        server.start_server()

    finally:
        updater.stop_updating()


if __name__ == '__main__':
    main()
