
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Attendance, AttendancePassword
from .serializers import AttendanceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Swagger response schemas
attendance_success_response = openapi.Response(
    description="Success",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "success": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether the operation was successful"),
        },
    ),
)

attendance_status_response = openapi.Response(
    description="Attendance status",
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "attended": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether the user attended"),
        },
    ),
)

@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["user_id", "password"],
        properties={
            "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="User ID"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Attendance password"),
        },
    )
)
def post(self, request):
    user_id = request.data.get('user_id')
    password = request.data.get('password')
    today = timezone.now().date()
    if not user_id or not password:
        return Response({'error': 'user_id and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        pw_obj = AttendancePassword.objects.get(date=today)
    except AttendancePassword.DoesNotExist:
        return Response({'error': 'No password set for today.'}, status=status.HTTP_400_BAD_REQUEST)
    if not pw_obj.check_password(password):
        return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
    attendance, created = Attendance.objects.get_or_create(user_id=user_id, date=today)
    attendance.attended = True
    attendance.save()
    return Response({'success': True})
class SubmitAttendanceView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id", "password"],
            properties={
                "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="User ID"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Attendance password"),
            },
        ),
        responses={200: attendance_success_response}
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        password = request.data.get('password')
        today = timezone.now().date()
        if not user_id or not password:
            return Response({'error': 'user_id and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pw_obj = AttendancePassword.objects.get(date=today)
        except AttendancePassword.DoesNotExist:
            return Response({'error': 'No password set for today.'}, status=status.HTTP_400_BAD_REQUEST)
        if not pw_obj.check_password(password):
            return Response({'error': 'Incorrect password.'}, status=status.HTTP_401_UNAUTHORIZED)
        attendance, created = Attendance.objects.get_or_create(user_id=user_id, date=today)
        attendance.attended = True
        attendance.save()
        return Response({'success': True})

class AttendanceStatusView(APIView):
    @swagger_auto_schema(
        responses={200: attendance_status_response}
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        today = timezone.now().date()
        try:
            attendance = Attendance.objects.get(user_id=user_id, date=today)
            return Response({'attended': attendance.attended})
        except Attendance.DoesNotExist:
            return Response({'attended': False})

# Admin endpoint to set/change password
class SetAttendancePasswordView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["password"],
            properties={
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password to set for today"),
                "date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Date (YYYY-MM-DD), optional"),
            },
        ),
        responses={200: attendance_success_response}
    )
    def post(self, request):
        password = request.data.get('password')
        date = request.data.get('date')
        if not password:
            return Response({'error': 'password is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if date:
            date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
        AttendancePassword.set_password(password, date)
        return Response({'success': True})
    # Admin endpoint to set/change password
    class SetAttendancePasswordView(APIView):
        @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=["password"],
                properties={
                    "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password to set for today"),
                    "date": openapi.Schema(type=openapi.TYPE_STRING, format="date", description="Date (YYYY-MM-DD), optional"),
                },
            )
        )
        def post(self, request):
            password = request.data.get('password')
            date = request.data.get('date')
            if not password:
                return Response({'error': 'password is required.'}, status=status.HTTP_400_BAD_REQUEST)
            if date:
                date = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            AttendancePassword.set_password(password, date)
            return Response({'success': True})
