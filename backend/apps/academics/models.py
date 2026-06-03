from django.db import models

class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True) # e.g. 2025-26
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'course')

    def __str__(self):
        return f"{self.name} ({self.course.name})"
