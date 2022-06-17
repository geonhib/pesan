from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.validators import MinValueValidator
from django.urls import reverse
from core.validators import image_validator, expire_now_or_future


class SaccoManager(models.Manager):
    """class to filter sacco model objects"""
    def get_sacco(self):
        business = Sacco.objects.filter(status='active')
        return business

STATUS = (
    ('active', 'active'),
    ('inactive', 'inactive')
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


PRICES = (
    ('120000', '120000'),
    ('240000', '240000')
)
class Package(CustomModel):
    # TODO Ensure packages always exist.
    name = models.CharField(max_length=60, unique=True)
    capacity = models.PositiveIntegerField()
    price = models.CharField(max_length=9, choices=PRICES, default='120000')
    status = models.CharField(max_length=10, default='active')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('package_detail', kwargs={'pk': self.pk})


class Sacco(CustomModel):
    """"
    The core model for this application.
    """
    name = models.CharField(max_length=80, unique=True)
    package = models.ForeignKey(Package, null=True, on_delete=models.SET_NULL, related_name='bussiness_package')  # TODO Set package to default rather than null
    district = models.CharField(max_length=60, null=True, blank=True,)
    location = models.CharField(max_length=60, null=True, blank=True,)
    email = models.EmailField(null=True, blank=True, unique=True)  
    telephone = models.CharField(max_length=60, blank=True, null=True, unique=True)
    # website = models.URLField(null=True, blank=True)
    director = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='bussiness_director', blank=True,)
    status = models.CharField(max_length=10, default='inactive')
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


# class SaccoUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     business = models.ForeignKey(Business, on_delete=models.PROTECT)


class License(CustomModel):
    key = models.CharField(max_length=80, unique=True)
    sacco = models.ForeignKey(Sacco, null=True, on_delete=models.SET_NULL, related_name='business_license')
    expiry_date = models.DateTimeField(auto_now_add=False, auto_now=False, validators=[expire_now_or_future])
    status = models.CharField(max_length=10, choices=STATUS, default='active')

    class Meta:
        ordering = ['-created_on', '-updated_on']
        unique_together = ['key', 'sacco']

    def __str__(self):
        return f"{self.sacco} - {self.expiry_date}" 