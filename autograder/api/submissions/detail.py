from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from autograder.apps.runtests.models import Submission


class SubmissionDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sid):
        sub = get_object_or_404(Submission, id=sid)
        if sub.usr != request.user and not request.user.is_staff:
            return Response({"error": "You do not have permission to view this submission."}, status=403)
        data = {
            "id": sub.id,
            "language": sub.language,
            "code": sub.code,
            "verdict": sub.verdict,
            "runtime": sub.runtime,
            "timestamp": sub.timestamp,
            "usr": sub.usr.username,
            "contest": str(sub.contest) if sub.contest_id else None,
            "problem": str(sub.problem) if sub.problem_id else None,
            "problem_id": sub.problem_id,
            "insight": sub.insight if request.user.is_staff else None,
        }
        return Response(data)
