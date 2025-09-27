from rest_framework import serializers
from autograder.apps.problems.models import Problem

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = [
            "id", "name", "contest", "points", "statement", "inputtxt", "outputtxt", "samples", "tl", "ml", "interactive", "secret", "testcases_zip", "has_simulation", "simulation_name"
        ]