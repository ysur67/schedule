from rest_framework import serializers

from apps.timetables.models.group import EducationalLevel, Group


class EducationalLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EducationalLevel
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"
