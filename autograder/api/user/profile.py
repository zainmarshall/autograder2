
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .profile_serializer import UserProfileSerializer, UserProfileUpdateSerializer
from autograder.apps.index.models import GraderUser
from django.shortcuts import get_object_or_404

# Public profile view (read-only)
class UserPublicProfileAPI(APIView):
    permission_classes = []  # Allow any

    def get(self, request, uid):
        user = get_object_or_404(GraderUser, username=uid)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)



class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserProfileUpdateSerializer, responses={200: UserProfileSerializer})
    def post(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)
