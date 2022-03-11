from rest_framework import serializers

from apps.timetables.models.subject import Subject


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"
