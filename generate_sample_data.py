import os
import django
import sys
import random

# Setup Django environment
sys.path.append(os.path.join(os.getcwd(), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.users.models import Teacher, Student
from apps.academics.models import Course, Subject, AcademicYear
from django.utils import timezone

User = get_user_model()

def create_sample_data():
    print("Starting sample data generation...")

    # 1. Create Academic Year
    year_name = "2026-27"
    academic_year, created = AcademicYear.objects.get_or_create(
        name=year_name,
        defaults={
            'start_date': '2026-04-01',
            'end_date': '2027-03-31',
            'is_active': True
        }
    )
    if created: print(f"Created Academic Year: {year_name}")

    # 2. Define Classes and Subjects
    classes = [
        "Kindergarten", "Nursery", "LKG", "UKG",
        "Grade 1", "Grade 2", "Grade 3", "Grade 4",
        "Grade 5", "Grade 6", "Grade 7", "Grade 8"
    ]

    base_subjects = [
        "English", "Hindi", "Mathematics", "Science", 
        "Social Science", "Computer", "GK", "Drawing"
    ]

    # 3. Create Teachers
    teacher_data = [
        {"username": "sharma_v", "first_name": "Vijay", "last_name": "Sharma", "qual": "M.Sc B.Ed"},
        {"username": "verma_a", "first_name": "Anjali", "last_name": "Verma", "qual": "MA English"},
        {"username": "singh_r", "first_name": "Rajesh", "last_name": "Singh", "qual": "MCA"},
        {"username": "kaur_p", "first_name": "Priya", "last_name": "Kaur", "qual": "B.Sc B.Ed"},
        {"username": "gupta_s", "first_name": "Sanjay", "last_name": "Gupta", "qual": "B.Com B.Ed"},
    ]

    teachers = []
    for td in teacher_data:
        user, created = User.objects.get_or_create(
            username=td['username'],
            defaults={
                'first_name': td['first_name'],
                'last_name': td['last_name'],
                'email': f"{td['username']}@example.com",
                'role': 'TEACHER',
                'is_approved': True
            }
        )
        if created:
            user.set_password('pass1234')
            user.save()
        
        teacher, _ = Teacher.objects.get_or_create(
            user=user,
            defaults={'qualification': td['qual'], 'experience_years': random.randint(2, 15)}
        )
        teachers.append(teacher)
    
    print(f"Verified/Created {len(teachers)} Teachers.")

    # 4. Create Classes, Subjects and Students
    for class_name in classes:
        course, created = Course.objects.get_or_create(name=class_name)
        if created: print(f"Created Class: {class_name}")

        # Create Subjects for this class
        subject_objs = []
        for sub_name in base_subjects:
            subject, _ = Subject.objects.get_or_create(
                name=sub_name,
                course=course
            )
            subject_objs.append(subject)
            
            # Randomly assign a teacher to this subject if not already
            if not subject.teachers.exists():
                subject.teachers.add(random.choice(teachers))

        # Create 20 Students for this class
        for i in range(1, 21):
            stu_username = f"stu_{class_name.lower().replace(' ', '_')}_{i:02d}"
            user, created = User.objects.get_or_create(
                username=stu_username,
                defaults={
                    'first_name': f"Student",
                    'last_name': f"{class_name} {i}",
                    'email': f"{stu_username}@jsm.edu",
                    'role': 'STUDENT',
                    'is_approved': True
                }
            )
            if created:
                user.set_password('pass1234')
                user.save()

            # Ensure roll number is unique by including class name and index
            roll_num = f"{class_name.replace(' ', '')[:3].upper()}-{i:03d}-{random.randint(1000, 9999)}"
            Student.objects.get_or_create(
                user=user,
                defaults={
                    'course': course,
                    'roll_number': roll_num,
                    'parent_name': f"Parent of {user.first_name}",
                    'parent_phone': f"98765{random.randint(10000, 99999)}"
                }
            )
        print(f"Created 20 students for {class_name}")

    print("Sample data generation completed successfully!")

if __name__ == "__main__":
    create_sample_data()
