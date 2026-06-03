from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    qualification = models.CharField(max_length=200, blank=True)
    experience_years = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    subjects = models.ManyToManyField('academics.Subject', related_name='teachers', blank=True)

    def __str__(self):
        return f"Teacher: {self.user.get_full_name() or self.user.username}"

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    course = models.ForeignKey('academics.Course', on_delete=models.SET_NULL, null=True, related_name='students')
    roll_number = models.CharField(max_length=50, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    parent_name = models.CharField(max_length=200, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"Student: {self.user.get_full_name() or self.user.username} ({self.roll_number})"

class Parent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField(Student, related_name='parents', blank=True)

    def __str__(self):
        return f"Parent: {self.user.get_full_name() or self.user.username}"
