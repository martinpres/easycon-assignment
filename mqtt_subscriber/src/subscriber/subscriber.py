import json
import logging

from subscriber.model.message import Message


class Subscriber:

    def __init__(self, identifier, data_consumer, mqtt_client, mqtt_config):
        self._logger = logging.getLogger(__name__)
        self._identifier = identifier
        self._data_consumer = data_consumer

        self._mqtt_config = mqtt_config
        self._data_topic = self._mqtt_config.get('data_topic')

        def on_connect(client, userdata, flags, reason_code, properties):
            self._logger.info('MQTT client %s successfully connected', self._identifier)
            client.subscribe(self._data_topic)
            self._logger.info('MQTT client %s subscribed %s', self._identifier, self._data_topic)

        def on_message(client, userdata, msg):
            self._consume(msg)

        self._mqtt_client = mqtt_client
        self._mqtt_client.on_connect = on_connect
        self._mqtt_client.on_message = on_message

    def start_subscribing(self):
        self._mqtt_client.connect(
            self._mqtt_config.get('broker_url'),
            self._mqtt_config.get('broker_port')
        )

        self._mqtt_client.loop_forever()

    def stop_subscribing(self):
        self._mqtt_client.disconnect()
        self._logger.info('MQTT client %s disconnected', self._identifier)

    def _consume(self, message):
        self._logger.debug('MQTT client %s received message from topic %s', self._identifier, self._data_topic)
        payload = json.loads(message.payload)
        self._data_consumer.consume(Message(payload, message.topic))
