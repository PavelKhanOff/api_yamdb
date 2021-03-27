from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    get_confirmation_code, get_jwt_token)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
v1_auth_patterns = [
    path('mail/', get_confirmation_code),
    path('token/', get_jwt_token)
]
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(v1_auth_patterns))
]
