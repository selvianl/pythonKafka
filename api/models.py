from django.db import models


class Device(models.Model):
    device_id = models.CharField(
        max_length=255, unique=True
    )  # Unique identifier for the device
    name = models.CharField(max_length=255)  # Name of the device (optional)
    created_at = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp when the device was created

    def __str__(self):
        return self.device_id


class LocationData(models.Model):
    device = models.ForeignKey(
        Device, related_name="locations", on_delete=models.CASCADE
    )
    latitude = models.FloatField()  # Latitude coordinate
    longitude = models.FloatField()  # Longitude coordinate

    def __str__(self):
        return f"Device: {self.device.device_id}, Lat: {self.latitude}, Lon: {self.longitude}"
