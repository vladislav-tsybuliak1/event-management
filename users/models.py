from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import UserManager


class User(AbstractUser):

    email = models.EmailField(verbose_name="email address", unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()
