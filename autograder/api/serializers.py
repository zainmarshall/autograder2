from rest_framework import serializers
from autograder.apps.problems.models import Problem
from autograder.apps.index.models import GraderUser

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id", "name", "contest", "points", "statement", "inputtxt", "outputtxt", "samples", "tl", "ml", "interactive", "secret", "testcases_zip"
        ]

class GraderUserRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraderUser
        fields = [
            "id", "display_name", "index", "usaco_rating", "cf_rating", "inhouse"
        ]
