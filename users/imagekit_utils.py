from imagekitio import ImageKit
from django.conf import settings

imagekit = ImageKit(
    public_key=settings.IMAGEKIT['public_key'],
    private_key=settings.IMAGEKIT['private_key'],
    url_endpoint=settings.IMAGEKIT['url_endpoint']
)

def upload_image(file, file_name):
    options = type("Options", (object,), {"folder": "profile_pics/"})()
    return imagekit.upload(
        file=file,
        file_name=file_name,
        options=options
    )
