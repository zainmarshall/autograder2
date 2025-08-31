
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from ..oauth.decorators import login_required
from ..index.models import GraderUser

import logging

logger = logging.getLogger(__name__)





# old: HTML view for rankings
@login_required
def rankings_view(request, season):
    if settings.TJIOI_MODE:
        return redirect("contests:contests")

    if season != settings.CURRENT_SEASON:
        return redirect("rankings:rankings", season=settings.CURRENT_SEASON)

    rankings = [
        {
            "id": user.id,
            "name": user.display_name,
            "index": user.index,
            "usaco": user.usaco_rating,
            "cf": user.cf_rating,
            "inhouse": user.inhouse,
        }
        for user in GraderUser.objects.filter(is_tjioi=False, is_staff=False)
    ]

    rankings = [
        r for r in rankings if r["usaco"] > 800 or r["cf"] > 0 or r["inhouse"] > 0
    ]

    rankings.sort(key=lambda x: x["index"], reverse=True)
    for i in range(len(rankings)):
        rankings[i]["rank"] = i + 1

    context = {"rankings": rankings}

    return render(request, "rankings/rankings.html", context)

    def get(self, request, season):
        if settings.TJIOI_MODE:
            return Response({"error": "TJIOI mode enabled."}, status=403)
        if int(season) != settings.CURRENT_SEASON:
            return Response({"error": "Invalid season."}, status=400)
        users = GraderUser.objects.filter(is_tjioi=False, is_staff=False)
        serializer = GraderUserRankingSerializer(users, many=True)
        rankings = [r for r in serializer.data if r["usaco_rating"] > 800 or r["cf_rating"] > 0 or r["inhouse"] > 0]
        rankings.sort(key=lambda x: x["index"], reverse=True)
        for i, r in enumerate(rankings):
            r["rank"] = i + 1
        return Response({"rankings": rankings})
