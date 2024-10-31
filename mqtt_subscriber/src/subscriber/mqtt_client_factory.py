import ssl

import paho.mqtt.client as mqtt


def get_mqtt_client(client_id, security_config):
    if security_config is not None:
        client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        client.tls_set(security_config.get('ca_cert'), tls_version=ssl.PROTOCOL_TLSv1_2)
        client.tls_insecure_set(security_config.get('insecure', False))
        return client

    return mqtt.Client(client_id=client_id)
