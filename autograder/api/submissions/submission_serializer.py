from rest_framework import serializers
from autograder.apps.runtests.models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    usr = serializers.StringRelatedField()
    contest = serializers.StringRelatedField()
    problem = serializers.StringRelatedField()

    class Meta:
        model = Submission
        fields = [
            "id", "language", "code", "usr", "verdict", "runtime", "contest", "problem", "insight", "timestamp"
        ]