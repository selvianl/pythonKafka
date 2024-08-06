# api/tests.py

import unittest
from unittest.mock import MagicMock, patch

from django.test import TestCase

from graphene.test import Client

from api.models import Device
from gps.consumer import insert_gps_location, main

from .models import Device
from .schema import schema


class DeviceQueryTestCase(TestCase):
    def setUp(self):
        # Create test data
        Device.objects.create(device_id="1", name="Test Device 1")
        Device.objects.create(device_id="2", name="Test Device 2")

    def test_devices_query(self):
        client = Client(schema)
        query = """
        {
          devices {
            deviceId
            name
            createdAt
          }
        }
        """
        executed = client.execute(query)
        self.assertIsNone(executed.get("errors"))
        devices = executed["data"]["devices"]
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]["deviceId"], "1")
        self.assertEqual(devices[0]["name"], "Test Device 1")
        self.assertEqual(devices[1]["deviceId"], "2")
        self.assertEqual(devices[1]["name"], "Test Device 2")


class DeviceMutationTestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_create_device_mutation(self):
        mutation = """
        mutation createDevice($deviceId: String!, $name: String) {
          createDevice(deviceId: $deviceId, name: $name) {
            device {
              deviceId
              name
              createdAt
            }
          }
        }
        """
        variables = {"deviceId": "3", "name": "New Device"}
        executed = self.client.execute(mutation, variables=variables)
        self.assertIsNone(executed.get("errors"))
        device_data = executed["data"]["createDevice"]["device"]
        self.assertEqual(device_data["deviceId"], "3")
        self.assertEqual(device_data["name"], "New Device")

        # Verify the device is actually created in the database
        device = Device.objects.get(device_id="3")
        self.assertEqual(device.device_id, "3")
        self.assertEqual(device.name, "New Device")


class KafkaConsumerTestCase(TestCase):
    @patch("gps.consumer.KafkaConsumer")
    @patch("gps.consumer.insert_gps_location")
    def test_main(self, mock_insert_gps_location, MockKafkaConsumer):
        # Mock KafkaConsumer
        mock_consumer_instance = MagicMock()
        MockKafkaConsumer.return_value = mock_consumer_instance

        # Mock message
        mock_message = MagicMock()
        mock_message.value = {"latitude": 10.0, "longitude": 20.0}
        mock_consumer_instance.__iter__.return_value = [mock_message]

        main()

        # Check
        mock_insert_gps_location.assert_called_with(10.0, 20.0)

    @patch("gps.consumer.Device.objects.get_or_create")
    @patch("gps.consumer.LocationData.objects.create")
    def test_insert_gps_location(
        self, mock_create_location_data, mock_get_or_create_device
    ):
        mock_device = MagicMock()
        mock_get_or_create_device.return_value = (mock_device, True)

        insert_gps_location(10.0, 20.0)

        mock_get_or_create_device.assert_called_with(
            device_id="5", name="dev5"
        )

        mock_create_location_data.assert_called_with(
            device=mock_device, latitude=10.0, longitude=20.0
        )
