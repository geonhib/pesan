from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from .validators import image_validator, dob_validation
from django.core.validators import MinLengthValidator, MaxLengthValidator


class UserManager(BaseUserManager):
    """ User Model Manager """

    def create_user(self, email, password=None, is_staff=False, is_member=False, is_active=True):
        if not email:
            raise ValueError('Users must have email Address')
        if not password:
            raise ValueError('User must have Password')

        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_member = is_member
        user_obj.is_active = is_active
        user_obj.save(using=self._db)

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_member=False
        )
        return user


GENDER = (
    ('female', 'female'),
    ('male', 'male'),
)
MARITAL_STATUS = (
    ('single', 'single'),
    ('married', 'married'),
    ('divorced', 'divorced'),
)
EMPLOYER_TYPE = (
    ('unemmployed', 'unemployed'),
    ('self-employed', 'self-employed'),
    ('organization', 'organization'),
)
ID_TYPE = (
    ('national ID', 'national'),
    ('pasport', 'passport'),
    ('other', 'other'),
)
class User(AbstractBaseUser, PermissionsMixin):
    """Abastract Base User model"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)  
    telephone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    id_type = models.CharField(max_length=20, blank=True, choices=ID_TYPE, default='national')
    id_number = models.CharField(max_length=30, blank=True, null=True, validators=[MinLengthValidator(9), MaxLengthValidator(14)])
    photo = models.ImageField(upload_to='profile/', blank=True, null=True, validators=[image_validator])
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_previously_logged_in = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=MARITAL_STATUS, default='single')
    village = models.CharField(max_length=60, blank=True, null=True)
    date_of_birth = models.DateField(auto_now_add=False, auto_created=False, blank=True, null=True, validators=[dob_validation])
    gender = models.CharField(max_length=20, blank=True, choices=GENDER, default='single')
    next_of_kin_name = models.CharField(max_length=50, blank=True, null=True)
    next_of_kin_contact = models.CharField(max_length=50, blank=True, null=True)
    occupation = models.CharField(max_length=60, blank=True, null=True)
    employer_type = models.CharField(max_length=60, blank=True, choices=EMPLOYER_TYPE, default='organization')
    organization = models.CharField(max_length=80, blank=True, null=True)

    objects = UserManager() 

    class Meta:
        ordering = ['-date_joined', '-updated_at']

    def __str__(self):
        return self.email
        
    def get_full_name(self):
        if self.first_name and self.last_name:
            first_name=self.first_name.capitalize()
            last_name=self.last_name.capitalize()
            return f" {first_name} {last_name}"
        else:
            # return self.email.split('@')[0]
            return "No names provided."

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # def clean(self):
    #     pass

    # def clean(self):
    #     pass 

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})

    # other methods