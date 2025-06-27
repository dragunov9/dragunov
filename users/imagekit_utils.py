from imagekitio import ImageKit
from django.conf import settings

imagekit = ImageKit(
    public_key=settings.IMAGEKIT_PUBLIC_KEY,
    private_key=settings.IMAGEKIT_PRIVATE_KEY,
    url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
)

def upload_image_to_imagekit(file):
    upload = imagekit.upload(
        file=file,
        file_name=file.name
    )
    return upload.get('url')
