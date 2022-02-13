from rest_framework.routers import DefaultRouter
from apps.timetables.views import EducationalLevelViewSet

router = DefaultRouter()
router.register('educational-levels', EducationalLevelViewSet)

urlpatterns = router.urls
