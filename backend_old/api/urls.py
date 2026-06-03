from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CustomTokenObtainPairView, RegisterView, ProfileView,
                    UserViewSet, CourseViewSet, SubjectViewSet, StudentViewSet,
                    TeacherViewSet, ParentViewSet, AssignmentViewSet,
                    AttendanceViewSet, PaymentViewSet, VideoLectureViewSet,
                    AnnouncementViewSet, EventViewSet, GalleryViewSet,
                    ResultViewSet, NoteViewSet, EnquiryViewSet, dashboard_stats)
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'parents', ParentViewSet, basename='parent')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'video-lectures', VideoLectureViewSet, basename='video-lecture')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'events', EventViewSet, basename='event')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'results', ResultViewSet, basename='result')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'enquiries', EnquiryViewSet, basename='enquiry')

urlpatterns = [
    # Auth
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    # Dashboard
    path('dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    # All resource routes
    path('', include(router.urls)),
]
