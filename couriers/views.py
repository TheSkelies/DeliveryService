from django.shortcuts import render

from models.couriers import find_courier_by_id
from storage import load_couriers


def couriers(request):
    couriers_list = load_couriers("data/couriers.json")
    context = {"couriers": couriers_list}
    return render(request, "couriers/courier_list.html", context)


def courier_detail(request, courier_id):
    couriers_list = load_couriers("data/couriers.json")
    courier = find_courier_by_id(couriers_list, courier_id)
    context = {"courier": courier}
    return render(
        request,
        "couriers/courier_detail.html",
        context,
        status=404 if courier is None else 200,
    )