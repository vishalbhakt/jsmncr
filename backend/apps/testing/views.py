from rest_framework import viewsets, permissions
from core.utils import api_response
from .models import Quiz, Question, QuizAttempt
from .serializers import QuizSerializer, QuestionSerializer, QuizAttemptSerializer

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Quiz.objects.all()
        if user.role == 'TEACHER':
            return Quiz.objects.filter(teacher__user=user)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return Quiz.objects.filter(subject__course=student.course)
        return Quiz.objects.none()

    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        serializer.save(teacher=teacher)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)

class QuizAttemptViewSet(viewsets.ModelViewSet):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return QuizAttempt.objects.filter(student__user=user)
        if user.role in ['ADMIN', 'TEACHER']:
            return QuizAttempt.objects.all()
        return QuizAttempt.objects.none()

    def perform_create(self, serializer):
        student = getattr(self.request.user, 'student_profile', None)
        serializer.save(student=student)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)
