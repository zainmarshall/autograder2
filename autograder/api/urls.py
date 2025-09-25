from django.urls import path
from .problems.list import ProblemListAPI
from .problems.detail import ProblemDetailAPI
from .rankings.list import RankingsAPI
from .contests.list import ContestListAPI, ContestDetailAPI
from .contests.standings import ContestStandingsAPI
from .submissions.list import SubmissionListAPI
from .user.profile import UserProfileAPI, UserPublicProfileAPI
from .root import RootAPI

urlpatterns = [
    path("", RootAPI.as_view(), name="api-root"),
    path("problems/", ProblemListAPI.as_view(), name="api_problem_list"),
    path("problems/<int:pid>/", ProblemDetailAPI.as_view(), name="api_problem_detail"),
    path("rankings/<int:season>/", RankingsAPI.as_view(), name="api_rankings"),
    path("contests/", ContestListAPI.as_view(), name="api_contest_list"),
    path("contests/<int:cid>/", ContestDetailAPI.as_view(), name="api_contest_detail"),
    path("contests/<int:cid>/standings/", ContestStandingsAPI.as_view(), name="api_contest_standings"),
    path("submissions/", SubmissionListAPI.as_view(), name="api_submission_list"),
    path("user/", UserProfileAPI.as_view(), name="api-user-profile"),
    path("user/<str:uid>/", UserPublicProfileAPI.as_view(), name="api-user-public-profile"),
]
