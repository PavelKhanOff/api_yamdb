from django.db import models
from django.contrib.auth.models import (PermissionsMixin,
                                        AbstractBaseUser,
                                        BaseUserManager)
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class UserAccountManager(BaseUserManager):
    def create_user(self, email, role, username, password):
        user = self.model(
            email=email, role=role, username=username, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, username, password):
        user = self.create_user(
            email=email, role=role, username=username, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username_):
        print(username_)
        return self.get(username=username_)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=40, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=40, unique=True)
    role = models.CharField(
        max_length=30, verbose_name='role', default='user', null=True, blank=True)
    description = models.TextField(
        max_length=100, verbose_name='description', null=True, blank=True)
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role', 'email']

    objects = UserAccountManager()

    def get_short_name(self):
        return str(self.username)

    def natural_key(self):
        return str(self.username)

    def __str__(self):
        return str(self.username)


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
        related_name='categories',
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
    title = models.ForeignKey(
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
    title = models.ForeignKey(
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
