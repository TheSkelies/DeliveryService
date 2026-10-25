import sqlite3

from django.shortcuts import render

DB_PATH = "data/delivery.sqlite"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def couriers(request):
    conn = _conn()
    couriers_list = conn.execute(
        """
        SELECT
            c.id, c.name, c.phone, c.vehicle,
            c.departure_date, c.expected_delivery_date,
            c.capacity_kg, c.is_available,
            COALESCE(SUM(p.weight), 0) AS total_weight,
            COUNT(p.id) AS packages_count
        FROM couriers c
        LEFT JOIN packages p ON p.courier_id = c.id
        GROUP BY c.id
        ORDER BY c.name
        """
    ).fetchall()
    conn.close()
    return render(request, "couriers/courier_list.html", {"couriers": couriers_list})


def courier_detail(request, courier_id):
    conn = _conn()
    courier = conn.execute(
        "SELECT * FROM couriers WHERE id = ?",
        [courier_id],
    ).fetchone()
    packages_list = []
    if courier is not None:
        packages_list = conn.execute(
            """
            SELECT id, category, arrival_date, weight
            FROM packages
            WHERE courier_id = ?
            ORDER BY arrival_date
            """,
            [courier_id],
        ).fetchall()
    conn.close()
    return render(
        request,
        "couriers/courier_detail.html",
        {"courier": courier, "courier_packages": packages_list},
        status=404 if courier is None else 200,
    )


def couriers_free(request):
    booking_date = request.GET.get("date")
    free_list = []
    if booking_date:
        conn = _conn()
        free_list = conn.execute(
            """
            SELECT id, name, phone, vehicle,
                   capacity_kg
            FROM couriers
            WHERE is_available = 1
              AND expected_delivery_date = ?
            ORDER BY name
            """,
            [booking_date],
        ).fetchall()
        conn.close()
    return render(
        request,
        "couriers/couriers_free.html",
        {"couriers": free_list, "booking_date": booking_date},
    )