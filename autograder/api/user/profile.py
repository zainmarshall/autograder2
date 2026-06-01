from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .profile_serializer import UserProfileSerializer, UserProfileUpdateSerializer
from autograder.apps.index.models import GraderUser
from autograder.apps.index.views import get_codeforces_info, get_validation_settings
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
        user = request.user
        new_cf = (request.data.get("cf_handle") or "").strip() if "cf_handle" in request.data else None

        # CF handle validation: when user is changing their cf_handle (and validation enabled),
        # confirm the Codeforces account's first+last name matches display_name.
        if new_cf is not None and new_cf != (user.cf_handle or ""):
            vs = get_validation_settings()
            needs = vs.get("enforce_cf_handle_name_match", False) or (
                vs.get("enforce_cf_handle_for_samuel_zhang", False) and user.display_name == "Samuel Zhang"
            )
            if needs and new_cf:
                info = get_codeforces_info(new_cf)
                if not info:
                    return Response({"error": f"Could not retrieve Codeforces info for handle '{new_cf}'."}, status=400)
                first, last = info.get("firstName"), info.get("lastName")
                if not first or not last:
                    return Response({"error": "The Codeforces account must have both a first and last name set."}, status=400)
                cf_name = f"{first} {last}".strip()
                if cf_name.lower() != (user.display_name or "").lower():
                    return Response(
                        {"error": f"Codeforces name '{cf_name}' does not match your name '{user.display_name}'."},
                        status=400,
                    )

        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(user).data)
