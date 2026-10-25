from django.urls import path
from . import views

app_name = "packages"

urlpatterns = [
    path("", views.packages, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:package_id>/", views.package_detail, name="detail"),
]