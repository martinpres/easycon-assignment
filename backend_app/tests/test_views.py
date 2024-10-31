from unittest import TestCase
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class MQTTMetaDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-data-mqtt-meta')

    @patch('backend.webapi.views.MQTTMetaDataView.postgresql_service')
    def test_get_mqtt_metadata(self, mock_service):
        expected = [
            {
                'topic': 'test/topic',
                'mongo_id': 'mongo-1',
                'created_at': '2024-12-24T20:24:12.202412'
            },
            {
                'topic': 'test/topic',
                'mongo_id': 'mongo-2',
                'created_at': '2024-12-24T20:24:12.202412'
            },
            {
                'topic': 'test/topic',
                'mongo_id': 'mongo-2',
                'created_at': '2024-12-24T20:24:12.202412'
            }
        ]

        mock_service.list_metadata.return_value = expected

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)


class MQTTDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-data-mqtt')

    @patch('backend.webapi.views.MQTTDataView.mongodb_service')
    def test_get_mqtt_data(self, mock_service):
        expected = [
            {'some': 'value-1'},
            {'some': 'value-2'}
        ]

        mock_service.list_collection_content.return_value = expected

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)


class ModbusDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-data-modbus')

    @patch('backend.webapi.views.ModbusDataView.mongodb_service')
    def test_get_modbus_data(self, mock_service):
        expected = [
            {'some': 'value-1'},
            {'some': 'value-2'}
        ]

        mock_service.list_collection_content.return_value = expected

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected)


class ControlPublisherViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-control')

    @patch('backend.webapi.views.ControlPublisherView.mqtt_client')
    def test_post_success(self, mock_client):
        expected = {
            'command': 'start',
            'identifier': 'abc123'
        }

        response = self.client.post(self.url, expected, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_client.publish.assert_called_once_with(expected)
