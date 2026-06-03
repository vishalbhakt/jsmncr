from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.utils import api_response
from apps.users.models import Student, Teacher
from apps.academics.models import Course, Subject
from apps.activities.models import Assignment, Note, VideoLecture, Attendance
from apps.communication.models import Announcement, Event
from apps.finance.models import Payment
from apps.authentication.models import User
from apps.communication.serializers import AnnouncementSerializer
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    role = user.role
    
    data = {}
    
    if role == 'ADMIN' or user.is_superuser:
        data = {
            "total_students": Student.objects.count(),
            "total_teachers": Teacher.objects.count(),
            "total_courses": Course.objects.count(),
            "pending_approvals": User.objects.filter(is_approved=False, is_superuser=False).count(),
            "recent_announcements": AnnouncementSerializer(Announcement.objects.order_by('-created_at')[:5], many=True).data
        }
    elif role == 'TEACHER':
        teacher = getattr(user, 'teacher_profile', None)
        data = {
            "my_subjects": teacher.subjects.count() if teacher else 0,
            "my_assignments": Assignment.objects.filter(teacher=teacher).count() if teacher else 0,
            "total_students": Student.objects.count(), # Teachers can see school-wide count
            "recent_announcements": AnnouncementSerializer(Announcement.objects.filter(audience__in=['ALL', 'TEACHERS']).order_by('-created_at')[:5], many=True).data
        }
    elif role == 'STUDENT':
        student = getattr(user, 'student_profile', None)
        if student:
            att = Attendance.objects.filter(student=student)
            total = att.count()
            present = att.filter(status='Present').count()
            data = {
                "attendance_percentage": round((present/total)*100, 1) if total > 0 else 0,
                "pending_payments": Payment.objects.filter(student=student, status='Pending').count(),
                "my_assignments": Assignment.objects.filter(subject__course=student.course).count() if student.course else 0,
                "recent_announcements": AnnouncementSerializer(Announcement.objects.filter(audience__in=['ALL', 'STUDENTS']).order_by('-created_at')[:5], many=True).data
            }
            
    return api_response(data=data)
