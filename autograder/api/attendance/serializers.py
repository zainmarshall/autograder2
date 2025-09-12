from rest_framework import serializers
from .models import Attendance, AttendancePassword

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['user_id', 'date', 'attended']

class AttendancePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendancePassword
        fields = ['date', 'password_hash']
