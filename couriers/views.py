from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.couriers import find_courier_by_id
from storage import load_couriers


def couriers(request: HttpRequest) -> HttpResponse:
    couriers_list = load_couriers("data/couriers.json")

    if not couriers_list:
        content = """
<h1>Доставщики</h1>
<p class="text-muted">Доставщиков пока нет.</p>
"""
        return HttpResponse(page("Доставщики", content))

    items = ""
    for c in couriers_list:
        available_badge = (
            '<span class="badge bg-success">свободен</span>'
            if c.is_available
            else '<span class="badge bg-secondary">занят</span>'
        )
        items += f"""
<li class="list-group-item d-flex justify-content-between align-items-center">
  <div>
    <a href="/couriers/{c.id}/">#{c.id} {c.name}</a>
    <div class="small text-muted">
      выезд: {c.departure_date}, доставка: {c.expected_delivery_date},
      груз: {c.total_weight()}/{c.capacity_kg} кг
    </div>
  </div>
  {available_badge}
</li>"""

    content = f"""
<h1>Доставщики</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Доставщики", content))


def courier_detail(request: HttpRequest, courier_id: int) -> HttpResponse:
    couriers_list = load_couriers("data/couriers.json")
    courier = find_courier_by_id(couriers_list, courier_id)

    if courier is None:
        content = """
<h1 class="text-danger">Доставщик не найден</h1>
<a href="/couriers/" class="btn btn-outline-secondary">← к списку доставщиков</a>
"""
        return HttpResponse(
            page("Доставщик не найден", content),
            status=404,
        )

    if courier.packages:
        pkg_items = "".join(
            f'<li class="list-group-item"><a href="/packages/{p.id}/">'
            f"#{p.id} [{p.category}] — {p.weight} кг</a></li>"
            for p in courier.packages
        )
        packages_block = f'<ul class="list-group mb-3">{pkg_items}</ul>'
    else:
        packages_block = (
            '<p class="text-muted">Посылки не назначены</p>'
        )

    available_text = "свободен" if courier.is_available else "занят"
    available_badge = (
        "bg-success" if courier.is_available else "bg-secondary"
    )

    content = f"""
<div class="card">
  <div class="card-body">
    <h5 class="card-title">{courier.name}</h5>
    <p class="card-text"><strong>ID:</strong> {courier.id}</p>
    <p class="card-text"><strong>Телефон:</strong> {courier.phone}</p>
    <p class="card-text"><strong>Транспорт:</strong> {courier.vehicle}</p>
    <p class="card-text"><strong>Выезд:</strong> {courier.departure_date}</p>
    <p class="card-text"><strong>Примерная доставка:</strong> {courier.expected_delivery_date}</p>
    <p class="card-text">
      <strong>Загрузка:</strong> {courier.total_weight()} / {courier.capacity_kg} кг
    </p>
    <p class="card-text">
      <strong>Состояние:</strong>
      <span class="badge {available_badge}">{available_text}</span>
    </p>
    <h6>Назначенные посылки</h6>
    {packages_block}
    <a href="/couriers/" class="btn btn-outline-secondary">← к списку доставщиков</a>
  </div>
</div>
"""
    return HttpResponse(page(courier.name, content))