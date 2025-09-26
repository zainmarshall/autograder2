from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from autograder.apps.contests.utils import get_standings
from .standings_serializer import StandingsSerializer

class ContestStandingsAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request, cid):
        try:
            standings = get_standings(cid)
        except Exception as e:
            return Response({"error": str(e)}, status=404)
        serializer = StandingsSerializer(standings)
        return Response(serializer.data)
