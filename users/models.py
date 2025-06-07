from django.db import models
from django.contrib.auth.models import User
from .imagekit_utils import upload_image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='https://ik.imagekit.io/dragunov/default.jpg?updatedAt=1749255658947',
        upload_to='profile_pics'
    )

    def save(self, *args, **kwargs):
        if self.image and not self.image.url.startswith('http') and self.image.name != 'default.jpg':
            file_data = self.image.read()
            upload_response = upload_image(file_data, self.image.name)
            if upload_response.get("response") and upload_response["response"].get("url"):
                self.image = upload_response["response"]["url"]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'
