from django.http import HttpRequest, HttpResponse

from homepage.views import page
from models.packages import find_package_by_id
from storage import load_couriers, load_packages, load_users

DATA_DIR = "data"


def _load_all():
    users = load_users(f"{DATA_DIR}/users.json")
    couriers = load_couriers(f"{DATA_DIR}/couriers.json")
    packages = load_packages(f"{DATA_DIR}/packages.json", users, couriers)
    return users, couriers, packages


def packages(request: HttpRequest) -> HttpResponse:
    _, _, packages_list = _load_all()

    if not packages_list:
        content = """
<h1>Посылки</h1>
<p class="text-muted">Посылок пока нет.</p>
"""
        return HttpResponse(page("Посылки", content))

    items = ""
    for p in packages_list:
        sender = p.sender.name if p.sender else "—"
        recipient = p.recipient.name if p.recipient else "—"
        courier = p.courier.name if p.courier else "не назначен"
        items += f"""
<li class="list-group-item d-flex justify-content-between align-items-center">
  <div>
    <a href="/packages/{p.id}/">
      #{p.id} [{p.category}] {sender} → {recipient}
    </a>
    <div class="small text-muted">доставка: {p.arrival_date}, курьер: {courier}</div>
  </div>
  <span class="badge bg-secondary">{p.weight} кг</span>
</li>"""

    content = f"""
<h1>Посылки</h1>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("Посылки", content))


def package_detail(request: HttpRequest, package_id: int) -> HttpResponse:
    _, _, packages_list = _load_all()
    package = find_package_by_id(packages_list, package_id)

    if package is None:
        content = """
<h1 class="text-danger">Посылка не найдена</h1>
<a href="/packages/" class="btn btn-outline-secondary">← к списку посылок</a>
"""
        return HttpResponse(
            page("Посылка не найдена", content),
            status=404,
        )

    sender = package.sender.name if package.sender else "—"
    recipient = package.recipient.name if package.recipient else "—"
    courier = package.courier.name if package.courier else "не назначен"
    is_delivered = package.is_delivered()
    badge = "bg-success" if is_delivered else "bg-warning text-dark"
    status_text = "доставлена" if is_delivered else "в пути"

    content = f"""
<div class="card">
  <div class="card-body">
    <h5 class="card-title">Посылка #{package.id}</h5>
    <p class="card-text"><strong>Категория:</strong> {package.category}</p>
    <p class="card-text"><strong>Отправитель:</strong> {sender}</p>
    <p class="card-text"><strong>Получатель:</strong> {recipient}</p>
    <p class="card-text"><strong>Курьер:</strong> {courier}</p>
    <p class="card-text"><strong>Отправление:</strong> {package.departure_date}</p>
    <p class="card-text"><strong>Прибытие:</strong> {package.arrival_date}</p>
    <p class="card-text"><strong>Вес:</strong> {package.weight} кг</p>
    <p class="card-text">
      <strong>Статус:</strong> {package.status}
      <span class="badge {badge}">{status_text}</span>
    </p>
    <a href="/packages/" class="btn btn-outline-secondary">← к списку посылок</a>
  </div>
</div>
"""
    return HttpResponse(page(f"Посылка #{package.id}", content))