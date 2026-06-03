from rest_framework.routers import DefaultRouter
from apps.users.views import UserManagementViewSet, StudentViewSet, TeacherViewSet
from apps.academics.views import AcademicYearViewSet, CourseViewSet, SubjectViewSet
from apps.activities.views import AssignmentViewSet, NoteViewSet, VideoLectureViewSet, AttendanceViewSet, AssignmentSubmissionViewSet, VideoProgressViewSet
from apps.communication.views import AnnouncementViewSet, EventViewSet, GalleryImageViewSet, EnquiryViewSet
from apps.finance.views import PaymentViewSet
from apps.testing.views import QuizViewSet, QuizAttemptViewSet

router = DefaultRouter()

# Users
router.register(r'users', UserManagementViewSet, basename='user-management')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')

# Academics
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'subjects', SubjectViewSet, basename='subject')

# Activities
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'assignment-submissions', AssignmentSubmissionViewSet, basename='assignment-submission')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'video-lectures', VideoLectureViewSet, basename='video-lecture')
router.register(r'video-progress', VideoProgressViewSet, basename='video-progress')
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# Communication
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'events', EventViewSet, basename='event')
router.register(r'gallery', GalleryImageViewSet, basename='gallery')
router.register(r'enquiries', EnquiryViewSet, basename='enquiry')

# Testing
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'quiz-attempts', QuizAttemptViewSet, basename='quiz-attempt')

# Finance
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = router.urls
