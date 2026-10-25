import sqlite3

from django.shortcuts import render

DB_PATH = "data/delivery.sqlite"


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def packages(request):
    conn = _conn()
    packages_list = conn.execute(
        """
        SELECT
            p.id, p.category, p.arrival_date, p.weight, p.status,
            s.name AS sender_name,
            r.name AS recipient_name,
            c.name AS courier_name
        FROM packages p
        LEFT JOIN users    s ON p.sender_id    = s.id
        LEFT JOIN users    r ON p.recipient_id = r.id
        LEFT JOIN couriers c ON p.courier_id   = c.id
        ORDER BY p.id
        """
    ).fetchall()
    conn.close()
    return render(request, "packages/package_list.html", {"packages": packages_list})


def package_detail(request, package_id):
    conn = _conn()
    package = conn.execute(
        """
        SELECT
            p.id, p.category, p.departure_date, p.arrival_date,
            p.weight, p.status,
            s.name AS sender_name,
            r.name AS recipient_name,
            c.name AS courier_name
        FROM packages p
        LEFT JOIN users    s ON p.sender_id    = s.id
        LEFT JOIN users    r ON p.recipient_id = r.id
        LEFT JOIN couriers c ON p.courier_id   = c.id
        WHERE p.id = ?
        """,
        [package_id],
    ).fetchone()
    conn.close()
    return render(
        request,
        "packages/package_detail.html",
        {"package": package},
        status=404 if package is None else 200,
    )

def statistics(request):
    conn = _conn()
    by_category = conn.execute(
        """
        SELECT category, COUNT(*) AS total
        FROM packages
        GROUP BY category
        ORDER BY total DESC
        """
    ).fetchall()
    total = conn.execute(
        "SELECT COUNT(*) AS total FROM packages"
    ).fetchone()["total"]
    conn.close()
    return render(
        request,
        "packages/statistics.html",
        {"by_category": by_category, "total": total},
    )