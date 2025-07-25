from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        elif self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return '/media/default.jpg'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and self.image.name != 'default.jpg':
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception:
                pass  
