from django.contrib import admin

from couriers.models import Courier


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "vehicle", "availability", "capacity_kg",
    )
    list_filter = ("availability", "vehicle")
    search_fields = ("name", "phone")
    ordering = ("name",)
    list_per_page = 25