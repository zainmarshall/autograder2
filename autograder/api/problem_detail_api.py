from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from autograder.apps.problems.models import Problem
from django.conf import settings
from .serializers import ProblemSerializer

class ProblemDetailAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pid):
        try:
            problem = Problem.objects.get(id=pid)
        except Problem.DoesNotExist:
            return Response({"error": "Problem not found."}, status=404)
        if not request.user.is_staff and (problem.secret or not problem.contest or not problem.contest.tjioi == settings.TJIOI_MODE):
            return Response({"error": "Not authorized."}, status=403)
        serializer = ProblemSerializer(problem)
        return Response(serializer.data)
