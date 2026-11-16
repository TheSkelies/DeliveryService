from django.urls import path
from . import views

app_name = "packages"

urlpatterns = [
    path("", views.packages, name="list"),
    path("statistics/", views.statistics, name="statistics"),
    path("<slug:slug>/", views.package_detail, name="detail"),
]