from apps.timetables.models.classroom import Classroom
from rest_framework import serializers


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        exclude = ('is_active', )
