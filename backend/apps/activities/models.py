from django.db import models
from django.conf import settings

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='assignments')
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Graded', 'Graded'),
        ('Late', 'Late'),
    )
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Submitted')
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='notes')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='notes')
    file = models.FileField(upload_to='notes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VideoLecture(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='videos')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='videos')
    video_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VideoProgress(models.Model):
    video = models.ForeignKey(VideoLecture, on_delete=models.CASCADE, related_name='progress')
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='video_progress')
    watched_seconds = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    last_watched = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('video', 'student')

    def __str__(self):
        return f"{self.student.user.username} - {self.video.title}"

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Holiday', 'Holiday'),
    )
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='attendances')
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL, null=True, related_name='marked_attendances')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date', 'subject')

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"
