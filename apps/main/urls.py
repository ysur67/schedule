from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from apps.feedback.views import CurrentUserView
from apps.timetables.views import EducationalLevelViewSet

router = DefaultRouter()
router.register('educational-levels', EducationalLevelViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name="obtain_token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh_token"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('current-user/', CurrentUserView.as_view(), name="current_user"),
]
urlpatterns += router.urls
