import ssl

from pymodbus.client import ModbusTcpClient, ModbusTlsClient


def get_modbus_client(client_config):
    host = client_config.get('host')
    port = client_config.get('port')

    security_config = client_config.get('security')

    if security_config is None:
        return ModbusTcpClient(host=host, port=port)

    ssl_context = ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH,
        cafile=security_config.get('cafile')
    )

    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    if security_config.get('insecure', False):
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_OPTIONAL

    return ModbusTlsClient(host=host, port=port, sslctx=ssl_context)
