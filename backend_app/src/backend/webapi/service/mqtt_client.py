import atexit
import json
import ssl

import paho.mqtt.client as mqtt


class MqttClientService:

    def __init__(self, client_id, mqtt_config):
        self._client_id = client_id
        self._config = mqtt_config
        self._client = None

    def publish(self, data):
        if self._client is None:
            # Connects lazily
            self._connect()

        self._client.publish(self._config.get('control_topic'), json.dumps(data))

    def _connect(self):
        security_config = self._config.get('security')
        if security_config is None:
            self._client = mqtt.Client(client_id=self._client_id)

        else:
            self._client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=self._client_id)
            self._client.tls_set(security_config.get('ca_cert'), tls_version=ssl.PROTOCOL_TLSv1_2)
            self._client.tls_insecure_set(security_config.get('insecure', False))

        self._client.connect(self._config.get('broker_url'), self._config.get('broker_port'))

        atexit.register(self._client.disconnect)
