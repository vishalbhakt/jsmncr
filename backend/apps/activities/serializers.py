from rest_framework import serializers
from .models import Assignment, Note, VideoLecture, Attendance, AssignmentSubmission, VideoProgress

class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()
    is_submitted = serializers.SerializerMethodField()
    submission_details = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('teacher',)

    def get_teacher_name(self, obj):
        return obj.teacher.user.get_full_name() or obj.teacher.user.username

    def get_is_submitted(self, obj):
        user = self.context['request'].user
        if user.role == 'STUDENT':
            return obj.submissions.filter(student__user=user).exists()
        return False

    def get_submission_details(self, obj):
        user = self.context['request'].user
        if user.role == 'STUDENT':
            sub = obj.submissions.filter(student__user=user).first()
            if sub:
                return {
                    "id": sub.id,
                    "status": sub.status,
                    "marks": sub.marks,
                    "feedback": sub.feedback,
                    "submitted_at": sub.submitted_at
                }
        return None

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'
        read_only_fields = ('student',)

class NoteSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('teacher',)
    def get_teacher_name(self, obj):
        return obj.teacher.user.get_full_name() or obj.teacher.user.username

class VideoLectureSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.SerializerMethodField()
    class Meta:
        model = VideoLecture
        fields = '__all__'
        read_only_fields = ('teacher',)
    def get_teacher_name(self, obj):
        return obj.teacher.user.get_full_name() or obj.teacher.user.username

class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = '__all__'
        read_only_fields = ('student',)

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('marked_by',)
    def get_student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
