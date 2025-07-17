from django.shortcuts import render, redirect
from ..oauth.decorators import login_required, admin_required
from ..problems.models import Problem
from ..runtests.utils import submission_queue
import logging

logger = logging.getLogger(__name__)
# Create your views here.
@login_required
@admin_required
def admin_index_view(request):
    context = {
        "problems": Problem.objects.all().order_by("-id"),
        "newpid": Problem.objects.latest("id").id,
    }

    return render(request, "admintools/index.html", context)

@login_required
@admin_required
async def admin_skip_view(request, sid):
    await submission_queue.skip_submission(sid)

    return redirect("admintools:queue")

@login_required
@admin_required
async def admin_togglepause_view(request, paused):
    if paused == "running":
        logger.info("Attempting to pause the queue")
        submission_queue.toggle_pause(True) # pause the queue
    else:
        logger.info("Attempting to run the queue")
        submission_queue.toggle_pause(False) # run the queue
    return redirect("admintools:queue")

@login_required
@admin_required
def admin_queue_view(request):
    status = submission_queue.get_queue_status()

    context = {
        "submissions": status["queued_ids"],
        "is_paused": "paused" if status["is_paused"] else "running"
    }

    return render(request, "admintools/queue.html", context)