from django.contrib import admin
from .models import (User, Student, Teacher, Parent, Course, Subject,
                     Assignment, Attendance, Payment, VideoLecture,
                     Announcement, Event, Gallery, Result, Note, Enquiry)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_approved', 'date_joined')
    list_filter = ('role', 'is_approved')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} user(s) approved.')
    approve_users.short_description = 'Approve selected users'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_number', 'course', 'parent_name')
    search_fields = ('user__username', 'roll_number', 'parent_name')
    list_filter = ('course',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'experience_years')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    list_filter = ('course',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'due_date')
    list_filter = ('subject', 'teacher')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'marked_by')
    list_filter = ('status', 'date')
    search_fields = ('student__user__username',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'description', 'status', 'due_date')
    list_filter = ('status',)


@admin.register(VideoLecture)
class VideoLectureAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'created_at')
    list_filter = ('subject',)


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'audience', 'is_public', 'created_at')
    list_filter = ('audience', 'is_public')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_public')
    list_filter = ('is_public',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_name', 'marks_obtained', 'total_marks', 'date')
    list_filter = ('subject', 'exam_name')


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'created_at')
    list_filter = ('subject',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'parent_name', 'phone', 'class_applied', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'class_applied')
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
    mark_resolved.short_description = 'Mark as resolved'
