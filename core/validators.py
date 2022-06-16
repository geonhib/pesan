from django.utils import timezone
from django.core.exceptions import ValidationError


def image_validator(photo):
    """
    Ensures that an uploaded image does not exceed declared size.        
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB - 104857600
            250MB - 214958080
            500MB - 429916160
    """
    if photo:
        if photo.size > 2*1024*1024:
            raise ValidationError('Image too large, please select an image less than 2 mbs')
        else:
            return photo 
    else:
        ValidationError("Could not read image")


def expire_now_or_future(expiry_date):
    """Ensures expiry date is set to now or future date."""
    if expiry_date:
        if expiry_date < timezone.now():
            raise ValidationError('Expiry date should be now or in the future')
        else:
            return expiry_date
    else:
        ValidationError('Date not supplied')
