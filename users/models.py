from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.


class CustomUser(AbstractUser):
    profile_image = CloudinaryField(
        "profile_image",
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
