from apps.timetables.models.subject import Subject
from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        exclude = ('is_active', )
