from django.urls import path

from . import views

app_name = "runtests"

urlpatterns = [
    path('submit/', views.submit_view, name="submit"),
    path('submit/contest/<int:cid>/', views.submit_contest_view, name="submitcontest"),
    path('submit/problem/<int:pid>/', views.submit_problem_view, name="submitproblem"),
    path('status/<int:page>/', views.status_view, {'mine': False, 'cid': None}, name='status'),
    path('status/<int:cid>/<int:page>/', views.status_view, {'mine': False}, name='status'),
    path('status/mine/<int:page>/', views.status_view, {'mine': True, 'cid': None}, name='status'),
    path('status/mine/<int:cid>/<int:page>/', views.status_view, {'mine': True}, name='status'),
    path('status/submission/<int:id>/', views.submission_view, name="submission"),
    path('process_submit/', views.submit_post, name="submit_post")
]