from ..oauth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django_user_agents.utils import get_user_agent
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import GraderUser
from ..rankings.models import RatingChange

import logging

logger = logging.getLogger(__name__)
# Create your views here.


def mobile_home(request):
    user_agent = get_user_agent(request)

    if not user_agent.is_mobile:
        return redirect("/")
    return render(request, "index/mobile.html")


def index_view(request):
    if request.user.is_authenticated:
        return redirect("index:profile")

    context = {"tjioi": settings.TJIOI_MODE}
    return render(request, "index/index.html", context)


@login_required
def first_time_view(request):
    if not request.user.first_time:
        return redirect("index:profile")

    return render(request, "index/start.html")


@login_required
@require_POST
def update_first_time(request):
    email = request.POST.get("email", "").strip()
    request.user.personal_email = email
    request.user.first_time = False
    request.user.save()
    return redirect("index:profile")


@login_required
def profile_view(request):
    if request.user.first_time:
        return redirect("index:first_time")

    cfh = request.user.cf_handle

    context = {
        "cf_handle": cfh if cfh and len(cfh) > 0 else ""
    }
    return render(request, "index/profile.html", context=context)


@login_required
@require_POST
@csrf_exempt
def update_stats(request):
    usaco = request.POST.get("usaco_div", "").strip()
    cf = request.POST.get("cf_handle", "").strip()

    if usaco and usaco != "none":
        request.user.usaco_division = {
            "bronze": "Bronze",
            "silver": "Silver",
            "gold": "Gold",
            "plat": "Platinum",
        }.get(usaco, "Not Participated")
    else:
        request.user.usaco_division = "Not Participated"

    if cf is not None:
        request.user.cf_handle = cf

    request.user.save()

    response = redirect("index:profile")
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response["Access-Control-Allow-Credentials"] = "true"
    return response


@login_required
def info_view(request):
    context = {"active": "info", "tjioi": settings.TJIOI_MODE}
    return render(request, "index/info.html", context=context)


@login_required
def user_profile_view(request, id):
    user = get_object_or_404(GraderUser, pk=id)

    if settings.TJIOI_MODE and not request.user.is_staff:
        return redirect("index:profile")

    rating_changes = (
        RatingChange.objects.filter(user=user)
        .order_by("time")
        .values("id", "rating", "time")
    )

    context = {
        "name": user.display_name,
        "username": user.username,
        "cf": user.cf_handle,
        "usaco": user.usaco_division,
        "rating_changes": list(rating_changes),
        "no_rating_history": "false",
        "admin": request.user.is_staff,
    }

    if rating_changes.count() == 0:
        context["no_rating_history"] = "true"

    return render(request, "index/user_profile.html", context)


@login_required
def toggle_particles(request):
    user = request.user
    user.particles_enabled = not user.particles_enabled
    user.save()
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


@require_http_methods(["GET"])
@csrf_exempt
def api_user(request):
    """API endpoint to get current user data"""
    # Add CORS headers
    response = JsonResponse({})
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Access-Control-Allow-Headers"] = "Accept, Content-Type"

    if request.method == "OPTIONS":
        return response

    if request.user.is_authenticated:
        response = JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'display_name': request.user.display_name,
            'usaco_division': request.user.usaco_division,
            'cf_handle': request.user.cf_handle,
            'is_staff': request.user.is_staff,
            'particles_enabled': request.user.particles_enabled,
            'session_id': request.session.session_key,
            'backend': getattr(request.user, 'backend', None),
        })
    else:
        response = JsonResponse({
            'error': 'Not authenticated',
            'session_id': request.session.session_key,
            'session_keys': list(request.session.keys()),
        }, status=401)

    # Add CORS headers to the actual response
    response["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response["Access-Control-Allow-Credentials"] = "true"
    return response
