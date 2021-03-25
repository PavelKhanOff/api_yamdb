from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from .views import (
    SendMessage, SendToken,
    CategoryViewSet, GenreViewSet,
    TitleViewSet, CommentViewSet, ReviewViewSet
)

router = DefaultRouter()

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

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/email/', SendMessage, name='message_sending_view'),
    path('v1/auth/token/', SendToken, name='token_obtain_pair'),
]
