from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.utils import timezone

class AttendancePassword(models.Model):
    # Only one password per club/day, or you can extend as needed
    date = models.DateField(default=timezone.now, unique=True)
    password_hash = models.CharField(max_length=128)

    @classmethod
    def set_password(cls, raw_password, date=None):
        if date is None:
            date = timezone.now().date()
        obj, created = cls.objects.get_or_create(date=date)
        obj.password_hash = make_password(raw_password)
        obj.save()
        return obj

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

class Attendance(models.Model):
    user_id = models.CharField(max_length=128)  # Replace with ForeignKey if you have users
    date = models.DateField(default=timezone.now)
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_id', 'date')
