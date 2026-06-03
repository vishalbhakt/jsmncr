from rest_framework import serializers
from apps.authentication.serializers import UserSerializer
from apps.academics.models import Subject
from apps.academics.serializers import SubjectSerializer
from .models import Student, Teacher, Parent

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    subject_ids = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subjects',
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Teacher
        fields = '__all__'

    def update(self, instance, validated_data):
        subjects = validated_data.pop('subjects', None)
        instance = super().update(instance, validated_data)
        if subjects is not None:
            instance.subjects.set(subjects)
        return instance

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    class Meta:
        model = Student
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    children = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Parent
        fields = '__all__'
