from django.contrib import admin
from .models import Student, Teacher, Parent

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'roll_number')
    search_fields = ('user__username', 'user__first_name', 'roll_number')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'experience_years')
    search_fields = ('user__username', 'user__first_name')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('children',)
