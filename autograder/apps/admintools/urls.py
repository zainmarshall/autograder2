from django.urls import path

from . import views

app_name = "admintools"

urlpatterns = [
    path('', views.admin_index_view, name="index")
]
