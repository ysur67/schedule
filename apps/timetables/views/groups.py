from apps.timetables.serializers import (EducationalLevelSerializer,
                                         GroupSerializer)
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels
from apps.timetables.usecases.group import get_all_groups
from rest_framework.viewsets import ModelViewSet


class EducationalLevelViewSet(ModelViewSet):
    serializer_class = EducationalLevelSerializer
    queryset = get_all_educational_levels()


class GroupsViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = get_all_groups()
