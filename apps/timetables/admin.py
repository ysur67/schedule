from django.contrib import admin
from apps.timetables.models import Group, Teacher, EducationalLevel, Classroom, Lesson


@admin.register(Group)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(EducationalLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "time_start", "time_end")
