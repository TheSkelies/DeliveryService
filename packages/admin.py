from django.contrib import admin

from packages.models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "id", "category", "status", "weight",
        "sender", "recipient", "courier", "arrival_date",
    )
    list_filter = ("status", "category", "courier")
    search_fields = ("category", "sender__name", "recipient__name", "courier__name")
    list_select_related = ("sender", "recipient", "courier")
    ordering = ("id",)
    autocomplete_fields = ("sender", "recipient", "courier")
    list_per_page = 25