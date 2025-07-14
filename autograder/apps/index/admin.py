from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GraderUser
from django.forms import TextInput, Textarea
from django import forms

class GraderUserAdmin(UserAdmin):
    model = GraderUser
    list_display = ("id", "email", "display_name", "username", "usaco_division", "is_staff", "is_active", "is_tjioi", "cf_handle", "cf_rating", "grade", "personal_email")
    list_filter = ("is_staff", "is_superuser", "is_active", "is_tjioi")
    search_fields = ("id",)
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("display_name", "username", "usaco_division", "cf_handle", "cf_rating", "grade", "personal_email", "is_tjioi")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields":  ("email", "password1", "password2", "display_name", "username", "usaco_division", "is_staff", "is_active", "is_tjioi", "cf_handle", "cf_rating", "grade", "personal_email")}
        ),
    )

admin.site.register(GraderUser, GraderUserAdmin)