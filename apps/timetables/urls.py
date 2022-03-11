from rest_framework.routers import DefaultRouter

from apps.timetables.views import (EducationalLevelViewSet, GroupsViewSet,
                                   LessonViewSet, TeacherViewSet)

router = DefaultRouter()
router.register('groups', GroupsViewSet)
router.register('educational-levels', EducationalLevelViewSet)
router.register('teachers', TeacherViewSet)
router.register('lessons', LessonViewSet)

urlpatterns = router.urls
