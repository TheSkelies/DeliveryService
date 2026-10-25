from django.shortcuts import render

from models.packages import find_package_by_id
from storage import load_couriers, load_packages, load_users

DATA_DIR = "data"


def _load_all():
    users = load_users(f"{DATA_DIR}/users.json")
    couriers = load_couriers(f"{DATA_DIR}/couriers.json")
    packages = load_packages(f"{DATA_DIR}/packages.json", users, couriers)
    return packages


def packages(request):
    packages_list = _load_all()
    context = {"packages": packages_list}
    return render(request, "packages/package_list.html", context)


def package_detail(request, package_id):
    packages_list = _load_all()
    package = find_package_by_id(packages_list, package_id)
    context = {"package": package}
    return render(
        request,
        "packages/package_detail.html",
        context,
        status=404 if package is None else 200,
    )