from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date


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


def dob_validation(date_of_birth):
    """
    Check if a users date of birth is in allowed date range 
    """
    if date_of_birth:
        dob = date_of_birth
        upper_age = date(1920, 1, 1)
        lower_age = date(2004, 1, 1)

        if dob >= upper_age and dob < lower_age:
            return dob
        elif dob < upper_age:
            raise ValidationError('Sorry, you are a senior citizen therefore not eligible to use this system')
        elif dob > upper_age:
            raise ValidationError('Sorry, you are a child therefore not eligible to use this system')

    else:
        raise ValidationError('Date of birth not valid, use the format June 13, 2000 ')





