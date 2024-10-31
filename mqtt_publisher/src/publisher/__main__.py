import json
import logging
import logging.config
import os
import time
from argparse import ArgumentParser

from publisher.data_provider import DataProvider
from publisher.mqtt_client_factory import get_mqtt_client
from publisher import Publisher


def _parse_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)


def _setup_logging(config):
    log_config_path = os.path.join(config.get('log_config'))
    logging.config.fileConfig(log_config_path)


def main():
    argument_parser = ArgumentParser(
        prog='mqtt_publisher',
        description='Periodically reads data from public WEB API and publishes it to a MQTT topic.'
    )

    argument_parser.add_argument(
        '-i', '--id', required=True, type=str,
        help='identifier of the publisher'
    )

    argument_parser.add_argument(
        '-c', '--config', required=True, type=str,
        help='configuration JSON file'
    )

    args = argument_parser.parse_args()
    config = _parse_config(args.config)
    _setup_logging(config)

    data_provider = DataProvider(config.get('data_source'))
    mqtt_client = get_mqtt_client(args.id, config.get('mqtt', {}).get('security'))
    publisher = Publisher(args.id, data_provider, mqtt_client, config.get('mqtt'))

    try:
        publisher.start_publishing()
        while True:
            idle_time = publisher.idle_time()
            if idle_time is None:
                time.sleep(config.get("sleep_interval"))
            elif idle_time > 0:
                time.sleep(idle_time)

            publisher.run_once()

    finally:
        publisher.stop_publishing()


if __name__ == '__main__':
    main()
