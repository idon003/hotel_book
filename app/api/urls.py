from django.urls import path
from .views import (
    available_rooms,
    create_booking,
    my_bookings,
    cancel_booking,
    room_list,
    register,
    LoginView,
)

urlpatterns = [
    path("rooms/", room_list, name="room-list"),
    path("rooms/available/", available_rooms, name="available-rooms"),
    path("bookings/", create_booking, name="create-booking"),
    path("bookings/my/", my_bookings, name="my-bookings"),
    path("bookings/<int:booking_id>/cancel/", cancel_booking, name="cancel-booking"),
    path("auth/register/", register, name="register"),
    path("auth/login/", LoginView.as_view(), name=""),
]
