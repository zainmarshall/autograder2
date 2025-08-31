from rest_framework import serializers
from autograder.apps.problems.models import Problem
from autograder.apps.index.models import GraderUser
from autograder.apps.contests.models import Contest

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id", "name", "contest", "points", "statement", "inputtxt", "outputtxt", "samples", "tl", "ml", "interactive", "secret", "testcases_zip"
        ]

class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraderUser
        fields = [
            "id", "display_name", "index", "usaco_rating", "cf_rating", "inhouse"
        ]

class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = [
            "id", "name", "rated", "season", "tjioi", "start", "end", "editorial"
        ]
