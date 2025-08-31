from django.urls import path
from .problem_list_api import ProblemListAPI
from .problem_detail_api import ProblemDetailAPI
from .rankings_api import RankingsAPI
from .contest_api import ContestListAPI, ContestDetailAPI
from .submission_list_api import SubmissionListAPI

urlpatterns = [
    path("problems/", ProblemListAPI.as_view(), name="api_problem_list"),
    path("problems/<int:pid>/", ProblemDetailAPI.as_view(), name="api_problem_detail"),
    path("rankings/<int:season>/", RankingsAPI.as_view(), name="api_rankings"),
    path("contests/", ContestListAPI.as_view(), name="api_contest_list"),
    path("contests/<int:cid>/", ContestDetailAPI.as_view(), name="api_contest_detail"),
    path("submissions/", SubmissionListAPI.as_view(), name="api_submission_list"),
]
