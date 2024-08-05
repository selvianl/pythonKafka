import json
import os
import sys

from kafka import KafkaConsumer


sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django


django.setup()

from api.models import Device, LocationData
from core.config import KAFKA_BROKER, KAFKA_TOPIC


# Function to insert GPS location into PostgreSQL
def insert_gps_location(latitude, longitude):
    """Insert the GPS location into PostgreSQL."""
    try:
        device, _ = Device.objects.get_or_create(device_id="1", name="dev")
        log = LocationData.objects.create(
            device=device, latitude=latitude, longitude=longitude
        )

    except Exception as e:
        print(f"Error inserting to PostgreSQL: {e}")


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

    # Poll for messages
    for message in consumer:
        # Fetch the GPS data
        gps_data = message.value
        print(gps_data)
        latitude = gps_data["latitude"]
        longitude = gps_data["longitude"]

        # Insert GPS data into PostgreSQL
        insert_gps_location(latitude, longitude)


if __name__ == "__main__":
    main()
