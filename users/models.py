from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
# Create your models here.

DEFAULT_PROFILE_IMAGE = "https://res.cloudinary.com/dwbggpcgf/image/upload/v1738515996/oywv0ctnqnjvbi2ypcrt.png"


class CustomUser(AbstractUser):
    profile_image = CloudinaryField(
        "profile_image",
        blank=True,
        null=True,
        default=DEFAULT_PROFILE_IMAGE
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
