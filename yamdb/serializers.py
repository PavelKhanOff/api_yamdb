from rest_framework import serializers
from .models import (
    CustomUser, Review, Comment,
)
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainSerializer


class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date",)
        read_only_fields = ("id", "author", "pub_date",)
        model = Comment

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date",)
        read_only_fields = ("id", "author", "pub_date")
        model = Review
