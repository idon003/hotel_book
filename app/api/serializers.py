from rest_framework import serializers
from ..models import Room, Booking


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):

    total_cost = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "room", "check_in", "check_out", "total_cost"]

    def validate(self, data):
        room = data["room"]
        check_in = data["check_in"]
        check_out = data["check_out"]

        if check_in >= check_out:
            raise serializers.ValidationError(
                "День выезда должен быть позже дня заезда."
            )
        exists = Booking.objects.filter(
            room=room, check_in__lt=check_out, check_out__gt=check_in
        ).exists()
        if exists:
            raise serializers.ValidationError("Комната уже забронирована на эти даты.")
        return data

    def get_total_cost(self, obj):
        nights = (obj.check_out - obj.check_in).days
        return nights * obj.room.price_per_night


class MyBookingSerializer(serializers.ModelSerializer):
    room = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ("id", "room", "check_in", "check_out")


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def create(self, validated_data):
        from django.contrib.auth.models import User

        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
