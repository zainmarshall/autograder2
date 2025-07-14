from django.contrib import admin
from .models import Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'usr', 'contest', 'language',
        'verdict', 'runtime', 'memory', 'timestamp'
    )
    list_filter = ('verdict', 'language', 'contest', 'usr')
    search_fields = ('usr__username', 'problem', 'verdict')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

    fieldsets = (
        (None, {
            'fields': (
                'usr', 'problem', 'contest', 'language', 'code'
            )
        }),
        ('Result Info', {
            'fields': ('verdict', 'runtime', 'memory', 'timestamp', 'insight')
        }),
    )
