import json
import logging

import schedule


class Publisher:

    def __init__(self, identifier, data_provider, mqtt_client, mqtt_config):
        self._logger = logging.getLogger(__name__)
        self._identifier = identifier
        self._data_provider = data_provider

        self._mqtt_config = mqtt_config
        self._data_topic = self._mqtt_config.get('data_topic')
        self._control_topic = self._mqtt_config.get('control_topic')
        self._publish_interval = self._mqtt_config.get('publish_interval')

        def on_connect(client, userdata, flags, reason_code, properties):
            self._logger.info('MQTT client %s successfully connected', self._identifier)
            client.subscribe(self._control_topic)
            self._logger.info('MQTT client %s subscribed %s', self._identifier, self._control_topic)

        def on_message(client, userdata, msg):
            payload = msg.payload.decode('utf-8')
            self._logger.info(
                'MQTT client %s received message %s from topic %s', self._identifier, payload, self._control_topic)

            command = json.loads(payload)
            if command.get('identifier') != self._identifier:
                return
            match command.get('command'):
                case 'start':
                    self._schedule_job()
                case 'stop':
                    self._unschedule_job()

        self._mqtt_client = mqtt_client
        self._mqtt_client.on_connect = on_connect
        self._mqtt_client.on_message = on_message

    def start_publishing(self):
        self._mqtt_client.connect(
            self._mqtt_config.get('broker_url'),
            self._mqtt_config.get('broker_port')
        )

        self._mqtt_client.loop_start()
        self._schedule_job()

    def run_once(self):
        schedule.run_pending()

    def stop_publishing(self):
        self._unschedule_job()
        self._mqtt_client.loop_stop()
        self._mqtt_client.disconnect()
        self._logger.info('MQTT client %s disconnected', self._identifier)

    def idle_time(self):
        return schedule.idle_seconds()

    def _schedule_job(self):
        schedule.every(self._publish_interval).seconds.do(self._publish_api_data)
        self._logger.info('Publisher %s scheduled to run every %s seconds', self._identifier, self._publish_interval)

    def _unschedule_job(self):
        schedule.clear()
        self._logger.info('Publisher %s stopped', self._identifier)

    def _publish_api_data(self):
        data = self._data_provider.get()
        self._mqtt_client.publish(self._data_topic, json.dumps(data))
        self._logger.debug('Publisher %s published message to topic %s', self._identifier, self._data_topic)
