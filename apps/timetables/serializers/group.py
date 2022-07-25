from apps.timetables.models.group import EducationalLevel, Group
from rest_framework import serializers


class EducationalLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationalLevel
        exclude = ('is_active', )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        exclude = ('is_active', )
