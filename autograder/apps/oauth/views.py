from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@csrf_exempt
@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        request.user.access_token = None
        request.user.save()
    logout(request)
    return JsonResponse({'success': True})
