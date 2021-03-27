from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    get_confirmation_code,
    get_jwt_token,
    UserViewSet,
)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)


v1_auth_patterns = [
    path('mail/', get_confirmation_code),
    path('token/', get_jwt_token)
]

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include(v1_auth_patterns))
]
