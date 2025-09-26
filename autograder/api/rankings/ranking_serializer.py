from rest_framework import serializers
from autograder.apps.index.models import GraderUser

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraderUser
        fields = [
            "id", "display_name", "username", "index", "usaco_rating", "cf_rating", "inhouse"
        ]