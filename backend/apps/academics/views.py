from rest_framework import viewsets, permissions
from core.utils import api_response
from .models import AcademicYear, Course, Subject
from .serializers import AcademicYearSerializer, CourseSerializer, SubjectSerializer
from apps.authentication.permissions import IsAdmin

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [IsAdmin()]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)

class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Subject.objects.all()
        
        if user.is_superuser or user.role == 'ADMIN':
            return Subject.objects.all()
            
        if user.role == 'TEACHER':
            teacher_profile = getattr(user, 'teacher_profile', None)
            if teacher_profile:
                return teacher_profile.subjects.all()
            return Subject.objects.none()
            
        if user.role == 'STUDENT':
            student_profile = getattr(user, 'student_profile', None)
            if student_profile and student_profile.course:
                return Subject.objects.filter(course=student_profile.course)
            return Subject.objects.none()
            
        return Subject.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)
