from apps.timetables.models.group import EducationalLevel
from apps.timetables.serializers import (EducationalLevelSerializer,
                                         GroupSerializer)
from apps.timetables.usecases.educational_level import \
    get_all_educational_levels
from apps.timetables.usecases.group import (get_all_groups,
                                            get_groups_by_educational_level)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class EducationalLevelViewSet(ModelViewSet):
    serializer_class = EducationalLevelSerializer
    queryset = get_all_educational_levels()

    @action(methods=["GET"], detail=True, url_path="groups")
    def get_groups_by_level_view(self, request: HttpRequest, pk=None) -> Response:
        level = self.get_object()
        groups = get_groups_by_educational_level(level=level)
        serializer = self.get_serializer(groups, many=True)
        return Response(data=serializer.data)

    def get_serializer(self, *args, **kwargs):
        if self.action == 'get_groups_by_level_view':
            return GroupSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class GroupsViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = get_all_groups()
