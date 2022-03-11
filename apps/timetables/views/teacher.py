from apps.timetables.serializers.teacher import TeacherSerializer
from apps.timetables.usecases.teacher import get_all_teachers
from rest_framework.viewsets import ModelViewSet


class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = get_all_teachers()
