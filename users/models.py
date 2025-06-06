from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(
        default='https://ik.imagekit.io/dragunov/profile_pics/default.jpg?updatedAt=1749236584228'
    )

    def __str__(self):
        return f'{self.user.username} Profile'
