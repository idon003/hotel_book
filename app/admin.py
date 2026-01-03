from django.contrib import admin
from .models import Room, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity", "price_per_night")
    search_fields = ("name",)
    list_filter = ("capacity",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "guest", "check_in", "check_out")
    search_fields = ("guest__username", "room__name")
    list_filter = ("room", "check_in", "check_out")
