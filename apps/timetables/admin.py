from django.contrib import admin

from apps.timetables.models import (Classroom, EducationalLevel, Group, Lesson,
                                    Teacher)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "level",)
    list_filter = ("level",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(EducationalLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "group", "time_start", "time_end")
