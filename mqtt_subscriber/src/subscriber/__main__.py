import json
import logging
import logging.config
import os
from argparse import ArgumentParser

from subscriber.data_consumer import DataConsumer
from subscriber.mqtt_client_factory import get_mqtt_client
from subscriber import Subscriber


def _parse_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)


def _setup_logging(config):
    log_config_path = os.path.join(config.get('log_config'))
    logging.config.fileConfig(log_config_path)


def main():
    argument_parser = ArgumentParser(
        prog='mqtt_subscriber',
        description='Consumes data from MQTT topic and stores them to MongoDB and PostgreSQL databases.'
    )

    argument_parser.add_argument(
        '-i', '--id', required=True, type=str,
        help='identifier of the subscriber'
    )

    argument_parser.add_argument(
        '-c', '--config', required=True, type=str,
        help='configuration JSON file'
    )


    args = argument_parser.parse_args()
    config = _parse_config(args.config)
    _setup_logging(config)

    mqtt_client = get_mqtt_client(args.id, config.get('mqtt', {}).get('security'))
    data_consumer = DataConsumer(config.get('mongodb'), config.get('postgresql'))
    subscriber = Subscriber(args.id, data_consumer, mqtt_client, config.get('mqtt'))

    try:
        subscriber.start_subscribing()
    finally:
        subscriber.stop_subscribing()
        data_consumer.close()

if __name__ == '__main__':
    main()
