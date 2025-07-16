from django import forms
from django.contrib import admin
from .models import Problem


class ProblemAdminForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = "__all__"


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    form = ProblemAdminForm

    list_display = ("id", "name", "contest", "points", "interactive", "secret")
    list_filter = ("interactive", "secret", "contest")
    search_fields = ("name",)
    ordering = ("-id",)
    readonly_fields = ("id",)

    fieldsets = (
        (None, {"fields": ("name", "contest", "points")}),
        ("Limits", {"fields": ("tl", "ml")}),
        ("Flags", {"fields": ("interactive", "secret")}),
        (
            "Text Fields",
            {"fields": ("statement", "solution", "inputtxt", "outputtxt", "samples")},
        ),
    )
