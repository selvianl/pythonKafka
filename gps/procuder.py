import json
import os
import random
import sys
import time

from kafka import KafkaProducer


sys.path.append("/app")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django


django.setup()

from core.config import KAFKA_BROKER, KAFKA_TOPIC


# Function to generate simulated GPS coordinates
def generate_gps_data():
    # Here we are generating random latitude and longitude values for demonstration
    latitude = round(random.uniform(-90.0, 90.0), 6)
    longitude = round(random.uniform(-180.0, 180.0), 6)
    return latitude, longitude


# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode(
        "utf-8"
    ),  # Convert message to JSON format
)


def send_to_kafka(lat, lon):
    """Send GPS data to Kafka."""
    data = {"latitude": lat, "longitude": lon}
    producer.send(KAFKA_TOPIC, value=data)
    producer.flush()
    time.sleep(3)
    print(f"Sent to Kafka: {data}")


try:
    while True:
        try:
            lat, lon = generate_gps_data()
            latitude = float(lat)
            longitude = float(lon)

            # Send GPS data to Kafka
            send_to_kafka(latitude, longitude)
        except Exception as e:
            print(f"Error parsing message: {e}")
except Exception as e:
    print(f"Error parsing message: {e}")
