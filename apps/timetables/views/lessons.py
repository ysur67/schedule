from apps.timetables.serializers.lesson import LessonSerializer
from apps.timetables.usecases.lesson import get_all_lessons
from rest_framework.viewsets import ModelViewSet


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    queryset = get_all_lessons() \
        .select_related('group', 'teacher', 'classroom', 'subject')
