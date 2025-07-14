from django.contrib import admin
from .models import RatingChange

@admin.register(RatingChange)
class RatingChangeAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'rating', 'time')
    list_filter = ('time',)
    search_fields = ('userid__username',)
    ordering = ('-time',)
