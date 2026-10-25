from django.http import HttpRequest, HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
    "dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Общий HTML-каркас всех страниц проекта."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container">
    <a class="navbar-brand" href="/">Почтовый сервис</a>
    <div class="navbar-nav">
      <a class="nav-link" href="/packages/">Посылки</a>
      <a class="nav-link" href="/couriers/">Доставщики</a>
    </div>
  </div>
</nav>
<div class="container pb-5">
{content}
</div>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    content = """
<h1 class="display-4">Сервис учёта посылок</h1>
<p class="lead">Учёт отправлений, доставщиков и статусов посылок.</p>
<p>Основные разделы:</p>
<a href="/packages/" class="btn btn-primary me-2">Посылки</a>
<a href="/couriers/" class="btn btn-secondary">Доставщики</a>
"""
    return HttpResponse(page("Сервис учёта посылок", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    content = """
<h1 class="text-danger">404 — страница не найдена</h1>
<p>Проверьте адрес или вернитесь на главную.</p>
<a href="/" class="btn btn-primary">На главную</a>
"""
    return HttpResponse(
        page("404 — страница не найдена", content),
        status=404,
    )