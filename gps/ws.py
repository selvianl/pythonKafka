import logging
import random
import socket
import threading
import time


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def generate_gps_data():
    latitude = round(random.uniform(-90.0, 90.0), 6)
    longitude = round(random.uniform(-180.0, 180.0), 6)
    return latitude, longitude


def handle_client(client_socket):
    try:
        while True:
            lat, lon = generate_gps_data()
            message = f"{lat},{lon}\n"

            # Send the message to the client
            client_socket.sendall(message.encode("utf-8"))

            # Wait for 3 seconds before sending the next data
            time.sleep(3)
    except Exception as e:
        logger.info(f"Error with client: {e}")
    finally:
        client_socket.close()


def main():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)

    while True:
        client_socket, addr = server_socket.accept()
        # Start a new thread to handle the client
        client_handler = threading.Thread(
            target=handle_client, args=(client_socket,)
        )
        client_handler.start()


if __name__ == "__main__":
    main()
