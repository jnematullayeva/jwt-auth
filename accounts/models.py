from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    addres = models.CharField(max_length=120)


    def __str__(self):
        return self.username