from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from packages.models import Package


def packages(request):
    packages_qs = (
        Package.objects
        .select_related("sender", "recipient", "courier")
        .order_by("id")
    )
    context = {"packages": packages_qs}
    return render(request, "packages/package_list.html", context)


def package_detail(request, package_id):
    package = get_object_or_404(
        Package.objects.select_related("sender", "recipient", "courier"),
        pk=package_id,
    )
    return render(
        request, "packages/package_detail.html", {"package": package}
    )


def statistics(request):
    total = Package.objects.count()
    by_category = (
        Package.objects
        .values("category")
        .annotate(total=Count("id"))
        .order_by("-total")
    )
    context = {"total": total, "by_category": by_category}
    return render(request, "packages/statistics.html", context)