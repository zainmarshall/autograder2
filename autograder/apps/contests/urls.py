from django.urls import path

from . import views

app_name = "contests"

urlpatterns = [
    path("", views.contests_view, name="contests"),
    path("contest/<int:cid>/", views.contest_view, name="contest"),
    path(
        "contest/<int:cid>/standings/", views.contest_standings_view, name="standings"
    ),
    path(
        "contest/<int:cid>/status/<str:mine_only>/<int:page>/",
        views.contest_status_view,
        name="status",
    ),
]
