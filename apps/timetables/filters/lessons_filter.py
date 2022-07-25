from apps.timetables.models import Lesson
from django_filters.rest_framework import FilterSet, filters


class LessonsFilterSet(FilterSet):
    date = filters.DateFilter(field_name='date')

    class Meta:
        model = Lesson
        fields = ['date', ]
