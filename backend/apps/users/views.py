from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from core.utils import api_response
from apps.authentication.models import User
from apps.authentication.serializers import UserSerializer
from apps.authentication.permissions import IsAdmin
from .models import Student, Teacher, Parent
from .serializers import StudentSerializer, TeacherSerializer, ParentSerializer

class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = self.get_object()
        user.is_approved = True
        user.save()
        return api_response(data={"message": "User approved successfully."})

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending_users = self.get_queryset().filter(is_approved=False, is_superuser=False)
        serializer = self.get_serializer(pending_users, many=True)
        return api_response(data=serializer.data)

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN' or user.role == 'TEACHER':
            return Student.objects.all().select_related('user', 'course')
        if user.role == 'STUDENT':
            return Student.objects.filter(user=user).select_related('user', 'course')
        if user.role == 'PARENT':
            return Student.objects.filter(parents__user=user).select_related('user', 'course')
        return Student.objects.none()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        # All authenticated users can view the teacher list (for subject mapping etc)
        return Teacher.objects.all().select_related('user').prefetch_related('subjects')

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return api_response(success=False, error="Teacher profile not found", status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(teacher)
            return api_response(data=serializer.data)
        
        # Prevent teachers from updating their own subjects
        data = request.data.copy()
        if 'subjects' in data or 'subject_ids' in data:
            if not (request.user.is_superuser or request.user.role == 'ADMIN'):
                data.pop('subjects', None)
                data.pop('subject_ids', None)

        serializer = self.get_serializer(teacher, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return api_response(data=serializer.data)
        return api_response(success=False, error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)
