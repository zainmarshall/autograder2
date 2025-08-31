from django.urls import path

from . import views

app_name = "problems"

urlpatterns = [
    path("", views.problemset_view, name="problemset"),
    path("api/", views.problemset_api, name="problemset_api"),
    path("<int:pid>/", views.problem_view, name="problem"),
]
