from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, send_confirmation_code, obtain_token

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', send_confirmation_code),
    path('v1/auth/token/', obtain_token),
]
