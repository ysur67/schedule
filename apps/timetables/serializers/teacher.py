from apps.timetables.models.teacher import Teacher
from rest_framework import serializers


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        exclude = ('is_active', )
