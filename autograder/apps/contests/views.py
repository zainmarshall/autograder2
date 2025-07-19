from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
from ..oauth.decorators import login_required, admin_required
from .models import Contest
from ..problems.models import Problem
from ..index.models import GraderUser
from ..runtests.models import Submission
from .utils import get_standings
import logging

logger = logging.getLogger(__name__)


@login_required
def contests_view(request):
    contests = Contest.objects.filter(tjioi=settings.TJIOI_MODE).order_by("-start")
    context = {"contests": contests}
    return render(request, "contest/contests.html", context)


@login_required
def contest_view(request, cid):
    contest = get_object_or_404(Contest, pk=cid)

    problems = list(Problem.objects.filter(contest=contest).order_by('id'))
    if problems is None:
        problems = []

    now = timezone.now()
    contest_start = contest.start
    contest_end = contest.end
    time_message = contest_end
    time_type = "end"
    if now < contest_start:
        time_type = "start"
        time_message = contest_start

    ordered = []
    for problem in problems:
        ordered.append(
            {
                "name": problem.name,
                "problem": problem,
                "pid": problem.id,
                "points": getattr(problem, "points", 0),
                "solves": 0,
                "available": (
                    not getattr(problem, "secret", False) or request.user.is_staff
                ),
                "users": [],
            }
        )

    subs = Submission.objects.filter(contest=cid)
    users = list(GraderUser.objects.all())
    user_id_map = {user.id: idx for idx, user in enumerate(users)}

    for sub in subs:
        if sub.timestamp > contest_end:
            continue
        ind = user_id_map.get(sub.usr_id)
        pind = None
        for j, prob in enumerate(ordered):
            if prob["pid"] == getattr(sub, "problem_id", None):
                pind = j
                break
        if pind is None or ind is None:
            continue
        if sub.verdict in ["Accepted", "AC"]:
            if ind in ordered[pind]["users"]:
                continue
            ordered[pind]["solves"] += 1
            ordered[pind]["users"].append(ind)

    if ordered:
        context = {
            "title": contest.name,
            "problems": ordered,
            "user": request.user.id,
            "cid": contest.id,
            "timeStatus": time_message,
            "timeType": time_type,
            "editorial": getattr(contest, "editorial", None),
            "contest_over": timezone.now() > contest.end,
        }
        return render(request, "contest/contest.html", context)
    else:
        return redirect("contests:contests")


@login_required
def contest_standings_view(request, cid):
    standings = get_standings(cid)
    problems = Problem.objects.filter(contest_id=cid)
    contest = get_object_or_404(Contest, id=cid)

    context = {
        "title": standings["title"],
        "cid": cid,
        "pnum": standings["pnum"],
        "load": standings["load"],
        "problems": problems,
        "contest_over": timezone.now() > contest.end,
    }

    return render(request, "contest/standings.html", context)


@login_required
def contest_status_view(request, cid, mine_only, page):
    contest = get_object_or_404(Contest, id=cid)
    subs = Submission.objects.filter(contest=contest)

    if mine_only == "mine" or (
        timezone.now() < contest.end and not request.user.is_staff
    ):
        subs = subs.filter(usr=request.user)

    if not request.user.is_staff:
        subs = subs.filter(timestamp__gte=contest.start)

    subs = subs.order_by("-timestamp")

    # Pagination
    paginator = Paginator(subs, 25)  # Show 25 submissions per page
    page_number = page
    page_obj = paginator.get_page(page_number)

    context = {
        "title": contest.name,
        "user_id": request.user.id,
        "cid": cid,
        "page_obj": page_obj,
        "submissions": page_obj.object_list,
        "contest_over": timezone.now() > contest.end,
        "mine_only": mine_only,
    }
    return render(request, "contest/status.html", context)


@login_required
@admin_required
def contest_skip_view(request, sid, cid, mine_only, page):
    sub = get_object_or_404(Submission, id=sid)
    sub.verdict = "Skipped"
    sub.insight = "Your submission was manually skipped by an admin"
    sub.save()

    return redirect("contests:status", cid=cid, mine_only=mine_only, page=page)
