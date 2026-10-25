from django.urls import path

from . import views

app_name = "couriers"

urlpatterns = [
    path("", views.couriers, name="list"),
    path("<int:courier_id>/", views.courier_detail, name="detail"),
]