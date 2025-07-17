from django.urls import path

from . import views

app_name = "admintools"

urlpatterns = [
    path('', views.admin_index_view, name="index"),
    path('skip/<int:sid>/', views.admin_skip_view, name="skip"),
    path('togglepause/<str:paused>/', views.admin_togglepause_view, name="togglepause"),
    path('queue/', views.admin_queue_view, name="queue")
]
