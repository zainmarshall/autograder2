from django.shortcuts import render
from ..oauth.decorators import login_required, admin_required
from ..problems.models import Problem
# Create your views here.
@login_required
@admin_required
def admin_index_view(request):
    context = {
        "problems": Problem.objects.all().order_by("-id"),
        "newpid": Problem.objects.latest("id").id,
    }

    return render(request, "admintools/index.html", context)

