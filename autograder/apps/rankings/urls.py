from django.urls import path

from . import views

app_name = "rankings"

urlpatterns = [
    path("", views.rankings_view, {"season": None}, name="rankings"),
    path("<int:season>/", views.rankings_view, name="rankings"),
    path("api/<int:season>/", views.rankings_api, name="rankings_api"),
]
