from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'address', 'is_approved', 'profile_photo')

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_approved and not self.user.is_superuser:
            raise serializers.ValidationError("Account pending admin approval.")
        
        data['user'] = UserSerializer(self.user).data
        return data

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role', 'phone')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        from apps.users.models import Student, Teacher, Parent
        import random
        
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        
        # Create profile based on role
        if user.role == 'STUDENT':
            # Generate a random roll number for initial setup
            roll_no = f"ST-{random.randint(1000, 9999)}"
            Student.objects.create(user=user, roll_number=roll_no)
        elif user.role == 'TEACHER':
            Teacher.objects.create(user=user)
        elif user.role == 'PARENT':
            Parent.objects.create(user=user)
            
        return user
