from django.db import models
from django.conf import settings

class Announcement(models.Model):
    AUDIENCE_CHOICES = (
        ('ALL', 'All'),
        ('STUDENTS', 'Students'),
        ('TEACHERS', 'Teachers'),
        ('PARENTS', 'Parents'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='ALL')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, default='General') # e.g. Sports, Classroom, Event
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Image {self.id}"

class Enquiry(models.Model):
    student_name = models.CharField(max_length=200)
    parent_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    target_class = models.CharField(max_length=50) # e.g. Grade 5
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"Enquiry: {self.student_name} - {self.target_class}"
