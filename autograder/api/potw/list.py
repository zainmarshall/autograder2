from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from autograder.apps.index.models import ProblemOfTheWeek


def _serialize(potw):
    if potw is None:
        return None
    return {
        "level": potw.level,
        "title": potw.title,
        "link": potw.link,
    }


class POTWAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "beginner":     _serialize(ProblemOfTheWeek.objects.filter(level=ProblemOfTheWeek.BEGINNER).first()),
            "intermediate": _serialize(ProblemOfTheWeek.objects.filter(level=ProblemOfTheWeek.INTERMEDIATE).first()),
            "advanced":     _serialize(ProblemOfTheWeek.objects.filter(level=ProblemOfTheWeek.ADVANCED).first()),
        })
