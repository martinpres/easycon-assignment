from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.webapi.service.mongodb import MongoDbService
from backend.webapi.service.mqtt_client import MqttClientService
from backend.webapi.service.postgresql import PostgresqlService


class MQTTMetaDataView(APIView):
    postgresql_service = PostgresqlService(settings.POSTGRESQL)

    def get(self, request):
        return Response(self.postgresql_service.list_metadata())


class MQTTDataView(APIView):
    mongodb_service = MongoDbService(settings.MONGO_DB)

    def get(self, request):
        return Response(self.mongodb_service.list_collection_content('mqtt_data'))


class ModbusDataView(APIView):
    mongodb_service = MongoDbService(settings.MONGO_DB)

    def get(self, request):
        return Response(self.mongodb_service.list_collection_content('modbus_data'))


class ControlPublisherView(APIView):
    mqtt_client = MqttClientService(settings.MQTT_CLIENT_ID, settings.MQTT)

    def post(self, request):
        if 'command' not in request.data or 'identifier' not in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.mqtt_client.publish(request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
