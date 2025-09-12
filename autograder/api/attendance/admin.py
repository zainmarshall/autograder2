from django.contrib import admin
from .models import Attendance, AttendancePassword

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'attended')
    list_filter = ('date', 'attended')
    search_fields = ('user_id',)

@admin.register(AttendancePassword)
class AttendancePasswordAdmin(admin.ModelAdmin):
    list_display = ('date',)
    search_fields = ('date',)
