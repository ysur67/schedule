from rest_framework.routers import DefaultRouter

from apps.timetables.views import (EducationalLevelViewSet, GroupsViewSet,
                                   LessonViewSet, TeacherViewSet)

router = DefaultRouter()
router.register('groups', GroupsViewSet, basename="Group")
router.register('educational-levels',
                EducationalLevelViewSet, basename="EducationalLevel")
router.register('teachers', TeacherViewSet, basename="Teacher")
router.register('lessons', LessonViewSet, basename="Lesson")

urlpatterns = router.urls
