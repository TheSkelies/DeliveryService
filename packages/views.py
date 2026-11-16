from datetime import datetime

from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from packages.models import Package



SORT_FIELDS = {
    "id": "id",
    "category": "category",
    "weight": "weight",
    "arrival": "arrival_date",
}

def packages(request):
    qs = Package.objects.with_related()

    status = request.GET.get("status", "").strip()
    category = request.GET.get("category", "").strip()
    courier_id = request.GET.get("courier", "").strip()
    arrival = request.GET.get("arrival", "").strip()
    sort = request.GET.get("sort", "id")
    error = None

    if status:
        qs = qs.filter(status=status)
    if category:
        qs = qs.filter(category__icontains=category)
    if courier_id.isdigit():
        qs = qs.by_courier(int(courier_id))
    if arrival:
        try:
            qs = qs.arriving_on(datetime.strptime(arrival, "%Y-%m-%d").date())
        except ValueError:
            error = "Укажите корректную дату."

    sort_field = SORT_FIELDS.get(sort, "id")
    qs = qs.order_by(sort_field, "id")

    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "packages/package_list.html",
        {
            "packages": page_obj,
            "page_obj": page_obj,
            "status": status,
            "category": category,
            "courier_id": courier_id,
            "arrival": arrival,
            "sort": sort,
            "error": error,
        },
    )



def package_detail(request, slug):
    package = get_object_or_404(
        Package.objects.with_related(), slug=slug
    )
    return render(request, "packages/package_detail.html", {"package": package})


def statistics(request):
    by_status = (
        Package.objects
        .values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    by_category = (
        Package.objects
        .values("category")
        .annotate(
            total=Count("id"),
            active=Count("id", filter=Q(status=Package.Status.ACTIVE)),
            cancelled=Count("id", filter=Q(status=Package.Status.CANCELLED)),
            completed=Count("id", filter=Q(status=Package.Status.COMPLETED)),
        )
        .order_by("category")
    )

    return render(
        request,
        "packages/statistics.html",
        {"by_status": by_status, "by_category": by_category},
    )