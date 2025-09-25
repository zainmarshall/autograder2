from rest_framework import serializers
from autograder.apps.index.models import GraderUser


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraderUser
        fields = [
            "id", "email", "personal_email", "display_name", "username", "is_staff", "is_active",
            "usaco_division", "usaco_rating", "cf_handle", "cf_rating", "grade", "first_time", "is_tjioi",
            "author_drops", "inhouse", "index", "particles_enabled"
        ]


# For updates: all fields optional, so user can pick what to change
class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraderUser
        # Exclude read-only fields if needed, or allow all for now
        fields = [
            "email", "personal_email", "display_name", "usaco_division", "usaco_rating",
            "cf_handle", "cf_rating", "grade", "first_time", "is_tjioi",
            "author_drops", "inhouse", "index", "particles_enabled"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional for partial updates
        for field in self.fields.values():
            field.required = False
