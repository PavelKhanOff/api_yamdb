from django.db import models
from django.contrib.auth.models import (PermissionsMixin,
                                        AbstractBaseUser,
                                        BaseUserManager,
                                        AbstractUser)
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class UserRole(models.TextChoices):
    """Роли пользователей"""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CustomUser(AbstractUser):
    """Расширение стандартной модели пользователя Django"""
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=255,
        choices=UserRole.choices,
        default=UserRole.USER
        )


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
    )
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True,
    )
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[MaxValueValidator(datetime.now().year)],
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='catigories',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviewer'
    )
    title= models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    score = models.PositiveIntegerField(
        "Оценка", 
        null=False,
        validators=[
            MinValueValidator(1, "Не меньше 1"),
            MaxValueValidator(10, "Не больше 10")
        ]
    )

    class Meta:
        ordering = ("-pub_date",)


class Comment(models.Model):
    title= models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField(null=False)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)
