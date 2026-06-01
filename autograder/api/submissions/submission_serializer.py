from rest_framework import serializers
from autograder.apps.runtests.models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    usr = serializers.SerializerMethodField()
    def get_usr(self, obj):
        return obj.usr.username
    contest = serializers.StringRelatedField()
    problem = serializers.StringRelatedField()

    class Meta:
        model = Submission
        fields = [
            "id", "language", "code", "usr", "verdict", "runtime", "contest", "problem", "insight", "timestamp"
        ]