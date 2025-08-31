from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from autograder.apps.problems.models import Problem
from django.conf import settings
from .serializers import ProblemSerializer

class ProblemListAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        problems = Problem.objects.filter(contest__tjioi=settings.TJIOI_MODE)
        if not request.user.is_staff:
            problems = problems.filter(secret=False)
        problems = problems.order_by("-id")
        serializer = ProblemSerializer(problems, many=True)
        return Response({"problems": serializer.data})
