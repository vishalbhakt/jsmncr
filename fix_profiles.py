import os
import django
import sys

# Set up Django environment
sys.path.append('E:\\Work\\JSM_auth\\jsm\\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.authentication.models import User
from apps.users.models import Student, Teacher, Parent
import random

def fix_profiles():
    print("🛠️ Syncing User Profiles with Roles...\n")
    
    users = User.objects.all()
    count = 0
    
    for user in users:
        created = False
        if user.role == 'TEACHER':
            if not hasattr(user, 'teacher_profile'):
                Teacher.objects.create(user=user)
                created = True
        elif user.role == 'STUDENT':
            if not hasattr(user, 'student_profile'):
                roll_no = f"ST-{random.randint(1000, 9999)}"
                Student.objects.create(user=user, roll_number=roll_no)
                created = True
        elif user.role == 'PARENT':
            if not hasattr(user, 'parent_profile'):
                Parent.objects.create(user=user)
                created = True
        
        if created:
            print(f"✅ Created {user.role} profile for: {user.username}")
            count += 1
            
    print(f"\n✨ Sync complete. {count} profiles repaired.")

if __name__ == "__main__":
    fix_profiles()
