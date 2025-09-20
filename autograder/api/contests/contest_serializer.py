from rest_framework import serializers
from autograder.apps.contests.models import Contest

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = [
            "id", "name", "rated", "season", "tjioi", "start", "end", "editorial"
        ]