from django.db import models
from django.contrib.auth.models import User
from .imagekit_utils import upload_image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.URLField(
        default='https://ik.imagekit.io/dragunov/default.jpg?updatedAt=1749255658947',
    )

    def save(self, *args, **kwargs):
        
        if self.image and not str(self.image).startswith('http'):
            try:
                with open(self.image, 'rb') as f:
                    file_data = f.read()
                    upload_response = upload_image(file_data, os.path.basename(self.image))
                    if upload_response.response and upload_response.response.url:
                        self.image = upload_response.response.url
            except FileNotFoundError:
                pass  

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'
