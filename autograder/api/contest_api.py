from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from autograder.apps.contests.models import Contest
from django.conf import settings
from .serializers import ContestSerializer

class ContestListAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        contests = Contest.objects.filter(tjioi=settings.TJIOI_MODE)
        serializer = ContestSerializer(contests, many=True)
        return Response({"contests": serializer.data})

class ContestDetailAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request, cid):
        try:
            contest = Contest.objects.get(id=cid)
        except Contest.DoesNotExist:
            return Response({"error": "Contest not found."}, status=404)
        serializer = ContestSerializer(contest)
        return Response(serializer.data)
