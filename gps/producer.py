import json
import logging
import socket

from kafka import KafkaProducer


KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "iot"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Create a Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def send_to_kafka(lat, lon):
    """Send GPS data to Kafka."""
    data = {"latitude": lat, "longitude": lon}
    producer.send(KAFKA_TOPIC, value=data)
    producer.flush()
    logger.info(f"Sent to Kafka: {data}")


def main():
    # Connect to the TCP server
    server_host = "ws"
    server_port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # Decode the message
            message = data.decode("utf-8")

            try:
                parts = message.split(",")
                lat_part = parts[0]
                lon_part = parts[1]
                latitude = float(lat_part)
                longitude = float(lon_part)

                # Send GPS data to Kafka
                send_to_kafka(latitude, longitude)
            except Exception as e:
                logger.info(f"Error parsing message: {e}")
    except Exception as e:
        logger.info(f"Error with TCP connection: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
