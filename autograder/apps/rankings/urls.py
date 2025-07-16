from django.urls import path

from . import views

app_name = "rankings"

urlpatterns = [
    path("rankings/", views.rankings_view, {"season": None}, name="rankings"),
    path("rankings/<int:season>/", views.rankings_view, name="rankings"),
]
