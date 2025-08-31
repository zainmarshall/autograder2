from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from autograder.apps.index.models import GraderUser
from django.conf import settings
from .serializers import RankingSerializer

class RankingsAPI(APIView):
    permission_classes = [AllowAny]
    def get(self, request, season):
        if settings.TJIOI_MODE:
            return Response({"error": "TJIOI mode enabled."}, status=403)
        if int(season) != settings.CURRENT_SEASON:
            return Response({"error": "Invalid season."}, status=400)
        users = GraderUser.objects.filter(is_tjioi=False, is_staff=False)
        serializer = RankingSerializer(users, many=True)
        rankings = []
        for r in serializer.data:
            if r["usaco_rating"] > 800 or r["cf_rating"] > 0 or r["inhouse"] > 0:
                rankings.append({
                    "name": r["display_name"],
                    "usaco": r["usaco_rating"],
                    "cf": r["cf_rating"],
                    "inhouse": float(r["inhouse"]),
                    "index": float(r["index"]),
                })
        rankings.sort(key=lambda x: x["index"], reverse=True)
        for i, r in enumerate(rankings):
            r["rank"] = i + 1
        return Response({"rankings": rankings})
