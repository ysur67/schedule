from rest_framework import serializers
from apps.timetables.models.lesson import Lesson
from apps.timetables.serializers.classroom import ClassroomSerializer

from apps.timetables.serializers.group import GroupSerializer
from apps.timetables.serializers.subject import SubjectSerializer
from apps.timetables.serializers.teacher import TeacherSerializer


class LessonSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False)
    teacher = TeacherSerializer(many=False)
    classroom = ClassroomSerializer(many=False)
    subject = SubjectSerializer(many=False)

    class Meta:
        model = Lesson
        fields = "__all__"
