from django.db import models
from django.contrib.auth.models import AbstractUser



class WORKitUser(AbstractUser):
    GENDER_CHOICES = {
        "M": "Male",
        "F": "Female"
    }
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)



class Profile(models.Model):
    user = models.OneToOneField(WORKitUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics/", default="profile_pics/default.jpg")


    def __str__(self):
        return f"{self.user.username} Profile"
