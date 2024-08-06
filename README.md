## Summary

Project is written by using Python with Django framework.

Database is PostgreSQL. There is Kafka and Kafdrop integration.

WebSocket is generating random GPS data every 3 seconds and producer listens here.

After data received producer sends it to Kafka.

On the other side of Kafka queue there is consumer. It consumes queue and save incoming data to PostgreSQL.

## Update enviroment file
First update `.env` file to start-up. You can follow the `.env.example`.
Example `.env`:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_DB=test
DATABASE_PORT=5432

KAFKA_ADVERTISED_HOST_NAME=kafka
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
KAFKA_ADVERTISED_PORT=9092
KAFKA_DELETE_TOPIC_ENABLE=true
KAFKA_BROKER=kafka:9092
KAFKA_TOPIC=iot
```

## Dockerize

To dockerize project run following command;

    docker-compose build && docker-compose up    

After kafka pod is up create topic with the same value of `KAFKA_TOPIC` variable
Example:
```
docker exec -it kafka kafka-topics.sh --create --topic iot --partitions 1 --replication-factor 1 --bootstrap-server kafka:9092
```
and check with

```
docker exec -it kafka kafka-topics.sh --list --bootstrap-server kafka:9092
```

or you can go to `localhost:9000` and create via `Kafdrop` UI. After restart docker-compose.


# Reachable endpoints via:

 `http://localhost:8000/graphql` are:

## list all devices
```
{
  devices {
    deviceId
    name
    createdAt
  }
}
```
## get device
```
{
  device(deviceId: "5") {
    deviceId
    name
    createdAt
  }
}
```
## get location data of device
```
{
  locationData(deviceId: "5") {
    device {
      deviceId
      name
    }
    latitude
    longitude
  }
}
```
## create new device
```
mutation {
  createDevice(deviceId: "12", name: "Test 12 Device") {
    device {
      deviceId
      name
      createdAt
    }
  }
}
```

## update device
```
mutation {
  updateDevice(deviceId: "555", name: "Updated Test Device") {
    device {
      deviceId
      name
      createdAt
    }
  }
}
```

## delete device
```
mutation {
  deleteDevice(deviceId: "555") {
    success
  }
}
```