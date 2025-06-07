from django.db import models
from django.contrib.auth.models import User
from .imagekit_utils import upload_image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    upload_image_file = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    image = models.URLField(
        default='https://ik.imagekit.io/dragunov/default.jpg?updatedAt=1749255658947',
    )

    def save(self, *args, **kwargs):
        if self.upload_image_file:
            file_data = self.upload_image_file.read()
            filename = os.path.basename(self.upload_image_file.name)
            upload_response = upload_image(file_data, filename)
            if upload_response.response and upload_response.response.url:
                self.image = upload_response.response.url
            self.upload_image_file = None 

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'
