from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from autograder.apps.index.models import GraderUser
from django.conf import settings
from .ranking_serializer import RankingSerializer

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
            usaco_rating = int(r.get("usaco_rating", 0) or 0)
            cf_rating = int(r.get("cf_rating", 0) or 0)
            inhouse = float(r.get("inhouse", 0) or 0)
            index = float(r.get("index", 0) or 0)
            
            rankings.append({
                "name": r["display_name"],
                "username": r["username"],
                "usaco": usaco_rating,
                "cf": cf_rating,
                "inhouse": inhouse,
                "index": index,
            })
        
        rankings.sort(key=lambda x: x["index"], reverse=True)
        for i, r in enumerate(rankings):
            r["rank"] = i + 1
        return Response({"rankings": rankings})
