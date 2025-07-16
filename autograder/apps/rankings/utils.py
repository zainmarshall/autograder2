import requests
import logging
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from ..index.models import GraderUser
from ..contests.models import Contest
from ..contests.utils import get_standings
from .models import RatingChange

logger = logging.getLogger(__name__)


def get_codeforces_rating(user):
    handle = user.cf_handle
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)

    if response.status_code != 200:
        logger.warning("Failed to connect to Codeforces API.")
        return None

    data = response.json()
    if data["status"] == "OK":
        res = data["result"][0]["maxRating"]
        logger.info(
            f"Fetched cf rating of {res} from handle {handle} of user {user.username}"
        )
        return res
    else:
        logger.info(f"API error: {data['comment']}")
        return None


def update_rankings():
    users = GraderUser.objects.filter(is_tjioi=False, is_staff=False)

    usaco_map = {
        "Not Participated": 800,
        "Bronze": 800,
        "Silver": 1200,
        "Gold": 1600,
        "Platinum": 1900,
    }

    rankings = [
        {
            "id": user.id,
            "name": user.display_name,
            "usaco": usaco_map[user.usaco_division],
            "cf": user.cf_rating,
            "inhouses": [],
        }
        for user in users
    ]

    contests = Contest.objects.filter(rated=True, season=settings.CURRENT_SEASON)

    for contest in contests:
        contest_standings = get_standings(contest.id)
        for i in range(len(rankings)):
            took = False
            for j in range(len(contest_standings["load"])):
                if rankings[i]["id"] == contest_standings["load"][j]["id"]:
                    rankings[i]["inhouses"].append(
                        1200
                        * (
                            len(contest_standings["load"])
                            - contest_standings["load"][j]["rank"]
                            + 1
                        )
                        / len(contest_standings["load"])
                        + 800
                    )

                    took = True
                    break

            if not took:
                rankings[i]["inhouses"].append(0)

    for r in range(len(rankings)):
        rankings[r]["inhouses"].sort()

        drops = max(0, min(2, contests.count() - 2) + get_object_or_404(GraderUser, id=rankings[r]["id"]).author_drops)

        overall = 0
        for j in range(drops, contests.count()):
            overall += rankings[r]["inhouses"][j]

        if contests.count() > 0 and contests.count() - drops > 0:
            overall /= contests.count() - drops

        rankings[r]["inhouse"] = overall

        vals = [rankings[r]["usaco"], rankings[r]["cf"], rankings[r]["inhouse"]]
        vals.sort()

        rankings[r]["index"] = 0.2 * vals[0] + 0.35 * vals[1] + 0.45 * vals[2]

    
    rankings = [
        elem for elem in rankings
        if elem["usaco"] > 800 or elem["cf"] > 0 or elem["inhouse"] > 0
    ]

    rankings.sort(key=lambda x: x["index"], reverse=True)

    for i in range(len(rankings)):
        if i > 0 and rankings[i]["index"] == rankings[i - 1]["index"]:
            rankings[i]["rank"] = rankings[i - 1]["rank"]
        else:
            rankings[i]["rank"] = i + 1

    for r in rankings:
        user = get_object_or_404(GraderUser, id=r["id"])
        if abs(user.index - Decimal(str(r["index"]))) > Decimal("0.001"):
            RatingChange.objects.create(user=user, rating=r["index"])

        user.inhouses = r["inhouses"]
        user.inhouse = r["inhouse"]
        user.index = r["index"]
        user.rank = r["rank"]
        user.save()