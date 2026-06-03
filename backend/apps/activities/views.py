from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from core.utils import api_response
from .models import Assignment, Note, VideoLecture, Attendance, AssignmentSubmission, VideoProgress
from .serializers import (AssignmentSerializer, NoteSerializer, VideoLectureSerializer, 
                          AttendanceSerializer, AssignmentSubmissionSerializer, VideoProgressSerializer)

class ActivityBaseViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return api_response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return api_response(data=serializer.data, status=status.HTTP_201_CREATED)
        return api_response(success=False, error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return api_response(data=serializer.data)
        return api_response(success=False, error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return api_response(data={"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class AssignmentViewSet(ActivityBaseViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Assignment.objects.all()
        if user.role == 'TEACHER':
            return Assignment.objects.filter(teacher__user=user)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return Assignment.objects.filter(subject__course=student.course)
        return Assignment.objects.none()

    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if not teacher:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You must have a valid Teacher profile to perform this action.")
        serializer.save(teacher=teacher)


class AssignmentSubmissionViewSet(ActivityBaseViewSet):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return AssignmentSubmission.objects.all()
        if user.role == 'TEACHER':
            return AssignmentSubmission.objects.filter(assignment__teacher__user=user)
        if user.role == 'STUDENT':
            return AssignmentSubmission.objects.filter(student__user=user)
        return AssignmentSubmission.objects.none()

    def perform_create(self, serializer):
        student = getattr(self.request.user, 'student_profile', None)
        if not student:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You must have a valid Student profile to submit assignments.")
        serializer.save(student=student)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def grade(self, request, pk=None):
        if request.user.role not in ['ADMIN', 'TEACHER']:
            return api_response(success=False, error="Unauthorized", status=status.HTTP_403_FORBIDDEN)
        
        submission = self.get_object()
        serializer = self.get_serializer(submission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(status='Graded')
            return api_response(data=serializer.data)
        return api_response(success=False, error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(ActivityBaseViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Note.objects.all()
        if user.role == 'TEACHER':
            return Note.objects.filter(teacher__user=user)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return Note.objects.filter(subject__course=student.course)
        return Note.objects.none()

    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if not teacher:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You must have a valid Teacher profile to perform this action.")
        serializer.save(teacher=teacher)


class VideoLectureViewSet(ActivityBaseViewSet):
    serializer_class = VideoLectureSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return VideoLecture.objects.all()
        if user.role == 'TEACHER':
            return VideoLecture.objects.filter(teacher__user=user)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return VideoLecture.objects.filter(subject__course=student.course)
        return VideoLecture.objects.none()

    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if not teacher:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You must have a valid Teacher profile to perform this action.")
        serializer.save(teacher=teacher)


class VideoProgressViewSet(ActivityBaseViewSet):
    serializer_class = VideoProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'STUDENT':
            return VideoProgress.objects.filter(student__user=user)
        return VideoProgress.objects.none()

    def perform_create(self, serializer):
        student = getattr(self.request.user, 'student_profile', None)
        serializer.save(student=student)


class AttendanceViewSet(ActivityBaseViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Attendance.objects.all()
        if user.role == 'TEACHER':
            return Attendance.objects.filter(marked_by__user=user)
        if user.role == 'STUDENT':
            return Attendance.objects.filter(student__user=user)
        return Attendance.objects.none()

    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if not teacher:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You must have a valid Teacher profile to mark attendance.")
        serializer.save(marked_by=teacher)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def bulk_mark(self, request):
        if request.user.role not in ['ADMIN', 'TEACHER']:
            return api_response(success=False, error="Unauthorized", status=status.HTTP_403_FORBIDDEN)
        
        data = request.data # List of {student_id, status, date, subject_id}
        teacher = getattr(request.user, 'teacher_profile', None)
        
        created_count = 0
        for entry in data:
            Attendance.objects.update_or_create(
                student_id=entry['student'],
                date=entry['date'],
                subject_id=entry.get('subject'),
                defaults={'status': entry['status'], 'marked_by': teacher}
            )
            created_count += 1
            
        return api_response(data={"message": f"Successfully marked attendance for {created_count} students."})
