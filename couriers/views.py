from datetime import datetime

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, render

from couriers.models import Courier


def couriers(request):
    couriers_qs = (
        Courier.objects
        .annotate(
            packages_count=Count("packages"),
            total_weight=Sum("packages__weight"),
        )
        .order_by("name")
    )
    return render(request, "couriers/courier_list.html", {"couriers": couriers_qs})


def courier_detail(request, courier_id):
    courier = get_object_or_404(Courier, pk=courier_id)
    courier_packages = courier.packages.select_related(
        "sender", "recipient"
    ).order_by("arrival_date")
    return render(
        request,
        "couriers/courier_detail.html",
        {"courier": courier, "courier_packages": courier_packages},
    )


def couriers_free(request):
    raw_date = request.GET.get("date", "").strip()
    result = Courier.objects.none()
    error = None

    if raw_date:
        try:
            selected = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            result = (
                Courier.objects
                .filter(availability=Courier.Availability.AVAILABLE)
                .order_by("name")
            )

    return render(
        request,
        "couriers/couriers_free.html",
        {"couriers": result, "booking_date": raw_date, "error": error},
    )