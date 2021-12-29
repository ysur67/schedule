from django.contrib import admin
from apps.timetables.models import Group, Teacher, EducationalLevel


@admin.register(Group)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(EducationalLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    pass
