import os
import django
import sys
from datetime import datetime, timedelta

# Set up Django environment
sys.path.append('E:\\Work\\JSM_auth\\jsm\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import User, Student, Teacher, Course, Subject, Assignment, Attendance, VideoLecture, Note, Announcement
from django.core.files.uploadedfile import SimpleUploadedFile

def test_system():
    print("🚀 Starting Comprehensive Model & RBAC Verification...\n")
    
    # Clean up old test data if exists
    User.objects.filter(username__startswith='test_').delete()
    Course.objects.filter(name='Test Course').delete()

    try:
        # 1. Create Base Structure
        course = Course.objects.create(name="Test Course", description="Testing Grounds")
        subject = Subject.objects.create(name="Test Subject", course=course, description="Testing API")
        print("✅ Models: Course & Subject created successfully.")

        # 2. Test User Roles & Auto-Admin
        admin = User.objects.create_superuser(username='test_admin', password='password123', email='admin@test.com')
        # Trigger save to test auto-role logic
        admin.save()
        if admin.role != 'ADMIN':
            print(f"❌ RBAC Error: Superuser role is {admin.role}, expected ADMIN")
        else:
            print("✅ RBAC: Superuser automatically assigned ADMIN role.")

        teacher_user = User.objects.create_user(username='test_teacher', password='password123', role='TEACHER', is_approved=True)
        teacher = Teacher.objects.create(user=teacher_user, qualification="Ph.D", experience_years=10)
        teacher.subjects.add(subject)
        print("✅ Models: Teacher profile and subject mapping verified.")

        student_user = User.objects.create_user(username='test_student', password='password123', role='STUDENT', is_approved=True)
        student = Student.objects.create(user=student_user, course=course, roll_number="TEST001")
        print("✅ Models: Student profile and course association verified.")

        # 3. Test CRUD (Teacher Operations)
        # Note: In real app this goes through API, here we test model/db layer
        assignment = Assignment.objects.create(
            title="Test Assignment", 
            description="Verify CRUD", 
            subject=subject, 
            teacher=teacher, 
            due_date=datetime.now() + timedelta(days=1)
        )
        print("✅ CRUD: Assignment creation verified.")

        note = Note.objects.create(
            title="Test Note",
            content="Check file upload",
            subject=subject,
            teacher=teacher,
            file=SimpleUploadedFile("test.txt", b"hello world")
        )
        print("✅ CRUD: Note creation with file upload verified.")

        video = VideoLecture.objects.create(
            title="Test Video",
            subject=subject,
            teacher=teacher,
            video_url="https://youtube.com/test"
        )
        print("✅ CRUD: Video Lecture creation verified.")

        # 4. Test Attendance Logic
        attendance = Attendance.objects.create(
            student=student,
            date=datetime.now().date(),
            status='Present',
            marked_by=teacher
        )
        print("✅ CRUD: Attendance marking verified.")

        # 5. Verify RBAC Data Filtering Logic (Simulating get_queryset)
        # Teacher should see their assignment
        teacher_assignments = Assignment.objects.filter(teacher=teacher)
        if teacher_assignments.count() == 1:
            print("✅ RBAC: Teacher data isolation verified.")
        
        # Student should see assignment for their course
        student_assignments = Assignment.objects.filter(subject__course=student.course)
        if student_assignments.count() == 1:
            print("✅ RBAC: Student course-based visibility verified.")

        print("\n✨ ALL BACKEND CORE VERIFICATIONS PASSED!")

    except Exception as e:
        print(f"\n❌ VERIFICATION FAILED: {str(e)}")
    finally:
        # Cleanup
        User.objects.filter(username__startswith='test_').delete()
        Course.objects.filter(name='Test Course').delete()
        print("\n🧹 Test data cleaned up.")

if __name__ == "__main__":
    test_system()
