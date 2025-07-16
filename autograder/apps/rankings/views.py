from django.shortcuts import render, redirect
from django.conf import settings
from ..oauth.decorators import login_required
from ..index.models import GraderUser
from .utils import update_rankings


# Create your views here.
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
            "usaco": user.usaco_division,
            "cf": user.cf_rating,
            "inhouse": user.inhouse,
        }
        for user in GraderUser.objects.filter(is_tjioi=False, is_staff=False)
    ]
    rankings.sort(key=lambda x: x["index"], reverse=True)
    for i in range(len(rankings)):
        rankings[i]["rank"] = i + 1

    context = {"rankings": rankings, "user": request.user}

    return render(request, "rankings/rankings.html", context)
