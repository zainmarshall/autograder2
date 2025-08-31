from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from autograder.apps.runtests.models import Submission
from .serializers import SubmissionSerializer

class SubmissionListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        submissions = Submission.objects.filter(contest__tjioi=request.GET.get('tjioi', False))
        if not request.user.is_staff:
            submissions = submissions.filter(usr__is_staff=False)
        cid = request.GET.get('cid')
        if cid:
            submissions = submissions.filter(contest=cid)
        mine = request.GET.get('mine')
        if mine == 'true':
            submissions = submissions.filter(usr=request.user)
        submissions = submissions.order_by('-timestamp')
        paginator = PageNumberPagination()
        paginator.page_size = 25
        result_page = paginator.paginate_queryset(submissions, request)
        serializer = SubmissionSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
