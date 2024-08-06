import json
import logging
import os
import sys

from kafka import KafkaConsumer


sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django


django.setup()

from api.models import Device, LocationData
from core.config import KAFKA_BROKER, KAFKA_TOPIC


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def insert_gps_location(latitude, longitude):
    """Insert the GPS location into PostgreSQL."""
    try:
        device, _ = Device.objects.get_or_create(device_id="5", name="dev5")
        LocationData.objects.create(
            device=device, latitude=latitude, longitude=longitude
        )

    except Exception as e:
        logger.info(f"Error inserting to PostgreSQL: {e}")


def main():
    # Create Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(
            x.decode("utf-8")
        ),  # Deserialize JSON messages
    )

    for message in consumer:
        gps_data = message.value
        latitude = gps_data["latitude"]
        longitude = gps_data["longitude"]
        insert_gps_location(latitude, longitude)


if __name__ == "__main__":
    main()
