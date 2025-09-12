from .views import SubmitAttendanceView, AttendanceStatusView, SetAttendancePasswordView
from django.urls import path

urlpatterns = [
    path('submit/', SubmitAttendanceView.as_view(), name='attendance_submit'),
    path('status/', AttendanceStatusView.as_view(), name='attendance_status'),
    path('password/', SetAttendancePasswordView.as_view(), name='attendance_set_password'),
]
