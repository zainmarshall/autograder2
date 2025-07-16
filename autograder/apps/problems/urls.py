from django.urls import path

from . import views

app_name = "problems"

urlpatterns = [
    path("problemset/", views.problemset_view, name="problemset"),
    path("problem/<int:pid>/", views.problem_view, name="problem"),
]
