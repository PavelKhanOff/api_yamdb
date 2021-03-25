from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from .views import SendMessage, SendToken, CommentViewSet, ReviewViewSet

router = DefaultRouter()

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
    path('v1/auth/email/', SendMessage, name='message_sending_view'),
    path('v1/auth/token/', SendToken, name='token_obtain_pair'),
    path('', include(router.urls)),
]
