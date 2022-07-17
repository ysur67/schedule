from apps.timetables.filters.lessons_filter import LessonsFilterSet
from apps.timetables.serializers.lesson import LessonSerializer
from apps.timetables.usecases.lesson import get_all_lessons
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = LessonsFilterSet

    def get_queryset(self):
        return get_all_lessons() \
            .select_related('group', 'teacher', 'classroom', 'subject')
