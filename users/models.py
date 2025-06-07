from django.db import models
from django.contrib.auth.models import User
from .imagekit_utils import upload_image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='https://ik.imagekit.io/dragunov/default.jpg?updatedAt=1749255658947',
        upload_to='profile_pics'
    )

    def save(self, *args, **kwargs):
        
        if self.image and not str(self.image).startswith('http') and os.path.exists(self.image.path):
            with open(self.image.path, 'rb') as f:
                file_data = f.read()
                upload_response = upload_image(file_data, self.image.name)
                if upload_response.response and upload_response.response.url:
                    self.image = upload_response.response.url

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'
