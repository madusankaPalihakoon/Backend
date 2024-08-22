from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The username must be provided")
        if not email:
            raise ValueError("The email must be provided")
        if not password:
            raise ValueError("The password must be provided")
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('administrator', 'Administrator'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    username = models.CharField(db_index=True, unique=True, max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=240)
    mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES, default='user')

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"