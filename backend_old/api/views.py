from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count, Avg

from .models import (User, Student, Teacher, Parent, Course, Subject,
                     Assignment, Attendance, Payment, VideoLecture,
                     Announcement, Event, Gallery, Result, Note, Enquiry)
from .serializers import (UserSerializer, RegisterSerializer, StudentSerializer,
                          TeacherSerializer, ParentSerializer, CourseSerializer,
                          SubjectSerializer, AssignmentSerializer, AttendanceSerializer,
                          PaymentSerializer, VideoLectureSerializer, AnnouncementSerializer,
                          EventSerializer, GallerySerializer, ResultSerializer,
                          NoteSerializer, EnquirySerializer)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if not user.is_superuser and not user.is_approved:
            raise Exception('Account pending admin approval.')
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# --- Permissions ---

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'ADMIN'
        )

class IsTeacherUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'TEACHER'

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role in ['ADMIN', 'TEACHER']
        )


# --- ViewSets ---

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        user = self.get_object()
        user.is_approved = True
        user.save()
        return Response({'status': 'approved'})

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = User.objects.filter(is_approved=False, is_superuser=False)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Student.objects.all().select_related('user', 'course')
        if user.role == 'TEACHER':
            return Student.objects.all().select_related('user', 'course')
        if user.role == 'PARENT':
            parent_profile = getattr(user, 'parent_profile', None)
            if parent_profile:
                return parent_profile.children.all().select_related('user', 'course')
        if user.role == 'STUDENT':
            return Student.objects.filter(user=user).select_related('user', 'course')
        return Student.objects.none()


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.role in ['ADMIN', 'TEACHER'] or user.is_superuser:
            return Teacher.objects.all().select_related('user')
        return Teacher.objects.all().select_related('user') # Allow all to see teachers

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            teacher = Teacher.objects.get(user=request.user)
        except Teacher.DoesNotExist:
            return Response({'error': 'Teacher profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = self.get_serializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(teacher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentViewSet(viewsets.ModelViewSet):
    serializer_class = ParentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Parent.objects.all().select_related('user')
        if user.role == 'PARENT':
            return Parent.objects.filter(user=user).select_related('user')
        return Parent.objects.none()


class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacherOrAdmin]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Assignment.objects.all().select_related('subject', 'teacher__user').order_by('-created_at')
        
        if user.is_superuser or user.role == 'ADMIN':
            return qs
        if user.role == 'TEACHER':
            teacher = getattr(user, 'teacher_profile', None)
            return qs.filter(teacher=teacher)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return qs.filter(subject__course=student.course)
        if user.role == 'PARENT':
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(subject__course__students__parents=parent).distinct()
        return qs.none()
    
    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if teacher:
            serializer.save(teacher=teacher)
        else:
            serializer.save(teacher_id=self.request.data.get('teacher'))


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacherOrAdmin]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Attendance.objects.all().select_related('student__user').order_by('-date')
        
        if user.is_superuser or user.role == 'ADMIN':
            return qs
        if user.role == 'TEACHER':
            teacher = getattr(user, 'teacher_profile', None)
            return qs.filter(marked_by=teacher)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            return qs.filter(student=student)
        if user.role == 'PARENT':
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(student__parents=parent)
        return qs.none()
    
    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if teacher:
            serializer.save(marked_by=teacher)
        else:
            serializer.save()


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Payment.objects.all().order_by('-due_date')
        
        if user.is_superuser or user.role == 'ADMIN':
            return qs
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            return qs.filter(student=student)
        if user.role == 'PARENT':
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(student__parents=parent)
        return qs.none()


class VideoLectureViewSet(viewsets.ModelViewSet):
    serializer_class = VideoLectureSerializer
    permission_classes = [IsTeacherOrAdmin]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = VideoLecture.objects.all().select_related('subject', 'teacher__user').order_by('-created_at')
        
        if user.is_superuser or user.role == 'ADMIN':
            return qs
        if user.role == 'TEACHER':
            teacher = getattr(user, 'teacher_profile', None)
            return qs.filter(teacher=teacher)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return qs.filter(subject__course=student.course)
        if user.role == 'PARENT':
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(subject__course__students__parents=parent).distinct()
        return qs.none()
        
    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if teacher:
            serializer.save(teacher=teacher)
        else:
            serializer.save(teacher_id=self.request.data.get('teacher'))


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-created_at')
    serializer_class = AnnouncementSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Announcement.objects.all().order_by('-created_at')
        
        role_map = {'STUDENT': 'STUDENTS', 'TEACHER': 'TEACHERS', 'PARENT': 'PARENTS'}
        audience_tag = role_map.get(user.role, 'ALL')
        return Announcement.objects.filter(models.Q(audience='ALL') | models.Q(audience=audience_tag)).order_by('-created_at')


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('date')
    serializer_class = EventSerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all().order_by('-created_at')
    serializer_class = GallerySerializer
    pagination_class = None

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Result.objects.all().order_by('-date')
        
        if user.is_superuser or user.role == 'ADMIN':
            return qs
        if user.role == 'TEACHER':
            return qs # Teachers can see all results
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            return qs.filter(student=student)
        if user.role == 'PARENT':
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(student__parents=parent)
        return qs.none()


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [IsTeacherOrAdmin]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Note.objects.all().select_related('subject', 'teacher__user').order_by('-created_at')
        
        if user.is_superuser or user.role == 'ADMIN':
            return qs
        if user.role == 'TEACHER':
            teacher = getattr(user, 'teacher_profile', None)
            return qs.filter(teacher=teacher)
        if user.role == 'STUDENT':
            student = getattr(user, 'student_profile', None)
            if student and student.course:
                return qs.filter(subject__course=student.course)
        if user.role == 'PARENT':
            parent = getattr(user, 'parent_profile', None)
            if parent:
                return qs.filter(subject__course__students__parents=parent).distinct()
        return qs.none()
        
    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if teacher:
            serializer.save(teacher=teacher)
        else:
            serializer.save(teacher_id=self.request.data.get('teacher'))


class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer
    pagination_class = None

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """Return summary stats for the dashboard based on user role."""
    user = request.user

    if user.is_superuser or user.role == 'ADMIN':
        data = {
            'total_students': Student.objects.count(),
            'total_teachers': Teacher.objects.count(),
            'total_courses': Course.objects.count(),
            'pending_approvals': User.objects.filter(is_approved=False, is_superuser=False).count(),
            'total_enquiries': Enquiry.objects.count(),
            'recent_announcements': AnnouncementSerializer(
                Announcement.objects.order_by('-created_at')[:5], many=True
            ).data,
            'upcoming_events': EventSerializer(
                Event.objects.order_by('date')[:5], many=True
            ).data,
        }
    elif user.role == 'TEACHER':
        teacher = getattr(user, 'teacher_profile', None)
        data = {
            'total_students': Student.objects.count(),
            'my_subjects': SubjectSerializer(
                teacher.subjects.all(), many=True
            ).data if teacher else [],
            'my_assignments': Assignment.objects.filter(teacher=teacher).count() if teacher else 0,
            'recent_announcements': AnnouncementSerializer(
                Announcement.objects.order_by('-created_at')[:5], many=True
            ).data,
        }
    elif user.role == 'STUDENT':
        student = getattr(user, 'student_profile', None)
        if student:
            attendances = student.attendances.all()
            total = attendances.count()
            present = attendances.filter(status='Present').count()
            data = {
                'attendance_total': total,
                'attendance_present': present,
                'attendance_percentage': round(present / total * 100, 1) if total else 0,
                'pending_payments': student.payments.filter(status='Pending').count(),
                'recent_results': ResultSerializer(
                    student.results.order_by('-date')[:5], many=True
                ).data,
                'recent_announcements': AnnouncementSerializer(
                    Announcement.objects.filter(audience__in=['ALL', 'STUDENTS']).order_by('-created_at')[:5],
                    many=True
                ).data,
            }
        else:
            data = {'error': 'Student profile not found'}
    else:
        data = {'message': 'Welcome!'}

    return Response(data)
