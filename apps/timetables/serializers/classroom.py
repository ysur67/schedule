from rest_framework import serializers

from apps.timetables.models.classroom import Classroom


class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = "__all__"
