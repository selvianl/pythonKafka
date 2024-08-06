import graphene
from graphene_django.types import DjangoObjectType

from .models import Device, LocationData


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device
        fields = ("device_id", "name", "created_at")


class LocationDataType(DjangoObjectType):
    class Meta:
        model = LocationData
        fields = ("device", "latitude", "longitude")


class Query(graphene.ObjectType):
    devices = graphene.List(DeviceType)
    device = graphene.Field(
        DeviceType, device_id=graphene.String(required=True)
    )
    location_data = graphene.List(
        LocationDataType, device_id=graphene.String(required=True)
    )

    def resolve_devices(self, info, **kwargs):
        return Device.objects.all()

    def resolve_device(self, info, device_id):
        return Device.objects.get(device_id=device_id)

    def resolve_location_data(self, info, device_id):
        return LocationData.objects.filter(device__device_id=device_id)


class CreateDevice(graphene.Mutation):
    class Arguments:
        device_id = graphene.String(required=True)
        name = graphene.String()

    device = graphene.Field(DeviceType)

    def mutate(self, info, device_id, name=None):
        device = Device(device_id=device_id, name=name)
        device.save()
        return CreateDevice(device=device)


class UpdateDevice(graphene.Mutation):
    class Arguments:
        device_id = graphene.String(required=True)
        name = graphene.String()

    device = graphene.Field(DeviceType)

    def mutate(self, info, device_id, name=None):
        device = Device.objects.get(device_id=device_id)
        if name:
            device.name = name
        device.save()
        return UpdateDevice(device=device)


class DeleteDevice(graphene.Mutation):
    class Arguments:
        device_id = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, device_id):
        device = Device.objects.get(device_id=device_id)
        device.delete()
        return DeleteDevice(success=True)


class Mutation(graphene.ObjectType):
    create_device = CreateDevice.Field()
    update_device = UpdateDevice.Field()
    delete_device = DeleteDevice.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
