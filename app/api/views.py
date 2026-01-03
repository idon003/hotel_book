from django.contrib.auth import authenticate
from decimal import Decimal, InvalidOperation
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView


from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from ..models import Room, Booking
from .serializers import (
    RegisterSerializer,
    RoomSerializer,
    BookingSerializer,
    MyBookingSerializer,
    LoginSerializer,
)


@extend_schema(
    summary="Комнаты",
    description="Комнаты с возможностью фильтрации по цене и вместимости",
    parameters=[
        OpenApiParameter(
            name="min_price",
            type=OpenApiTypes.DECIMAL,
            location=OpenApiParameter.QUERY,
            description="Minimum price per night",
        ),
        OpenApiParameter(
            name="max_price",
            type=OpenApiTypes.DECIMAL,
            location=OpenApiParameter.QUERY,
            description="Maximum price per night",
        ),
        OpenApiParameter(
            name="capacity",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Minimum room capacity",
        ),
    ],
    responses={200: RoomSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def room_list(request):
    rooms = Room.objects.all()

    min_price = request.query_params.get("min_price")
    max_price = request.query_params.get("max_price")
    capacity = request.query_params.get("capacity")

    try:
        if min_price is not None:
            rooms = rooms.filter(price_per_night__gte=Decimal(min_price))

        if max_price is not None:
            rooms = rooms.filter(price_per_night__lte=Decimal(max_price))

    except InvalidOperation:
        return Response(
            {"ошибка": "Неверный формат цены"}, status=status.HTTP_400_BAD_REQUEST
        )

    if capacity is not None:
        if not capacity.isdigit():
            return Response(
                {"ошибка": "Неверный формат вместимости"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        rooms = rooms.filter(capacity__gte=int(capacity))

    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Возможные комнаты",
    description="Пустые комнаты на указанные даты",
    parameters=[
        OpenApiParameter(
            name="check_in",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
        OpenApiParameter(
            name="check_out",
            type=OpenApiTypes.DATE,
            location=OpenApiParameter.QUERY,
            required=True,
        ),
    ],
    responses={200: RoomSerializer(many=True)},
)
@api_view(["GET"])
def available_rooms(request):
    check_in = request.query_params.get("check_in", None)
    check_out = request.query_params.get("check_out", None)

    if not check_in or not check_out:
        return Response(
            {"ошибка": "Пожалуйста, укажите даты заезда и выезда."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    booked_rooms = Booking.objects.filter(
        check_in__lt=check_out, check_out__gt=check_in
    ).values_list("room_id", flat=True)

    available_rooms = Room.objects.exclude(id__in=booked_rooms)
    serializer = RoomSerializer(available_rooms, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Create booking",
    description="Create a new booking for a room",
    request=BookingSerializer,
    responses={201: BookingSerializer, 400: None},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_booking(request):
    serializer = BookingSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    booking = serializer.save(guest=request.user)
    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="My bookings",
    description="Retrieve bookings made by the authenticated user",
    responses={200: MyBookingSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = Booking.objects.filter(guest=request.user)
    serializer = MyBookingSerializer(bookings, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Отменить бронирование",
    description="Отменить бронирование по его ID",
    responses={204: None, 404: None},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, guest=request.user)
    except Booking.DoesNotExist:
        return Response(
            {"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND
        )

    booking.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    summary="Зарегистрироваться",
    description="Зарегистрироваться",
    request=RegisterSerializer,
    responses={201: RegisterSerializer, 400: None},
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    # TODO why cannot parse data?

    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "token": token.key,
        },
        status=status.HTTP_201_CREATED,
    )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Войти",
        description="Войти с именем пользователя и паролем",
        request=LoginSerializer,
        responses={200: LoginSerializer, 400: None},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"error": "Неверное имя пользователя или пароль."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "username": user.username,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
