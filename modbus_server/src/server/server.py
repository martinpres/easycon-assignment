import logging
import ssl

from pymodbus.server import StartTcpServer, StartTlsServer


class Server:

    def __init__(self, context, server_config):
        self._logger = logging.getLogger(__name__)
        self._context = context
        self._config = server_config
        self._address = (self._config.get('host'), self._config.get('port'))
        self._security_config = self._config.get('security')

    def start_server(self):

        if self._security_config is None:
            StartTcpServer(context=self._context, address=self._address)

        else:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(
                certfile=self._security_config.get('certfile'),
                keyfile=self._security_config.get('keyfile')
            )

            StartTlsServer(context=self._context, address=self._address, sslctx=ssl_context)