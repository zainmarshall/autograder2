from rest_framework.views import APIView
from rest_framework.response import Response

class RootAPI(APIView):
    def get(self, request):
        return Response({
            "message": "Welcome to the API root.",
            "endpoints": [
                "/problems/",
                "/problems/<int:pid>/",
                "/rankings/<int:season>/",
                "/contests/",
                "/contests/<int:cid>/",
                "/contests/<int:cid>/standings/",
                "/submissions/",
                "/user/",
                "/user/<str:uid>/"
            ]
        })