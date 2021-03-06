from datetime import datetime
from time import strftime
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import MinValueValidator
from django.urls import reverse
from core.validators import image_validator, expire_now_or_future
from django.utils import timezone
# from core.views import EmailThread


class SaccoManager(models.Manager):
    """class to filter sacco model objects"""
    def get_sacco(self):
        business = Sacco.objects.filter(status='active')
        return business

STATUS = (
    ('Active', 'active'),
    ('Inactive', 'inactive')
)
class CustomModel(models.Model):
    """
    An abstract base class model providing self-
    updating time and object author fields.
    """
    # status = models.CharField(max_length=10, default='inactive')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['created_on']


class Package(CustomModel):
    # TODO Ensure packages always exist.
    name = models.CharField(max_length=60, unique=True)
    capacity = models.PositiveIntegerField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(120000)], help_text='The minimum package price is 120,000/= per year ')
    status = models.CharField(max_length=10, default='active')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('package_detail', kwargs={'pk': self.pk})


SACCO_TYPE = (
    ('multipurpose', 'multipurpose'),
    ('savings', 'savings'),
    ('loans', 'loans'),
)
class Sacco(CustomModel):
    """"
    The core model for this application.
    """
    name = models.CharField(max_length=80, unique=True)
    type = models.CharField(max_length=40, choices=SACCO_TYPE, default='savings')
    tin = models.CharField(max_length=14, unique=True)
    package = models.ForeignKey(Package, null=True, on_delete=models.SET_NULL, related_name='bussiness_package')  # TODO Set package to default rather than null
    district = models.CharField(max_length=60, null=True, blank=True,)
    location = models.CharField(max_length=60, null=True, blank=True,)
    email = models.EmailField(null=True, blank=True, unique=True)  
    # website = models.URLField(null=True, blank=True)
    by_laws = models.FileField(upload_to='by_laws', null=True, blank=True, validators=[image_validator])
    permit = models.FileField(upload_to='permit',  validators=[image_validator])
    recommendation = models.FileField(upload_to='recommendation',  validators=[image_validator], help_text='Recommendation from LC1')
    incorporation = models.FileField(upload_to='certificates',  validators=[image_validator], help_text='Certificate of incorporation')
    status = models.CharField(max_length=10, default='inactive')
    director = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='business_director', blank=True,)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bussiness_creator')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bussiness_updater', null=True, blank=True)

    objects = models.Manager()
    filtered_objects = SaccoManager()
    
    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sacco_detail', kwargs={'pk': self.pk})


class SaccoUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='members')
    sacco = models.ForeignKey(Sacco, on_delete=models.RESTRICT, related_name='business')

    class Meta:
        # unique_together = ['user', 'sacco', ]
        verbose_name_plural = 'Sacco users'

    def __str__(self):
        return f"{self.user} - {self.sacco}"


class Trail(models.Model):
    sacco = models.ForeignKey(Sacco, blank=True, null=True, on_delete=models.SET_NULL)
    event = models.CharField(max_length=90, null=True)
    url = models.URLField(max_length=90, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse('trail_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.created_by} - {self.event}"

class License(CustomModel):
    key = models.CharField(max_length=80, unique=True)
    sacco = models.ForeignKey(Sacco, null=True, on_delete=models.SET_NULL, related_name='business_license')
    expiry_date = models.DateTimeField(auto_now_add=False, auto_now=False, validators=[expire_now_or_future])
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    class Meta:
        ordering = ['-created_on', '-updated_on']
        unique_together = ['key', 'sacco']

    def __str__(self):
        return f"{self.key}" 

    def save_sacco(self):
        print(self.sacco)
        self.sacco.save()

    def expiry_countdown(self):
        """
        Remind a director a before expiry of a license.
        Disabled expired licenses.
        Display days to license expiry.
        """
        DAYS_LEFT = (self.expiry_date - timezone.now()).days
        MONTH = 30
        DIRECTOR = self.sacco.director

        if DAYS_LEFT == 0:
            self.sacco.status = 'inactive'
            self.status = 'inactive'
            self.sacco.save()
            self.save()
            msg = f"License has expired."
            return msg
        elif DAYS_LEFT <= MONTH:
            msg = f"{DAYS_LEFT} days left, please renew."
            # TODO msgs, email, audit, notification
            return msg 
        else:
            msg = f"{DAYS_LEFT} days to go."
            return msg


