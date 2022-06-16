from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.forms import Form, ModelForm, DateField, widgets

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', ]


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=40)
    password = forms.CharField(max_length=40, widget=forms.PasswordInput)


CHOICES = (("1", "First"), ("2", "Second"))
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
class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'placeholder': 'Enter your surname'}))
    email = forms.CharField(label='Email address', widget=forms.TextInput(attrs={'placeholder': 'Enter email address'}))
    telephone = forms.CharField(label='Telephone', widget=forms.TextInput(attrs={'placeholder': 'Enter telephone number'}))
    id_type = forms.ChoiceField(label='ID type', widget=forms.Select, choices=ID_TYPE)
    id_number = forms.CharField(label='ID number', widget=forms.TextInput(attrs={'placeholder': 'Enter your ID number'}))
    gender = forms.CharField(label='gender', widget=forms.Select(attrs={'placeholder': 'Enter telephone number'}))
    next_of_kin_name = forms.CharField(label='Next of kin name', widget=forms.TextInput(attrs={'placeholder': 'Enter name of next of kin'}))
    next_of_kin_contact = forms.CharField(label='Next of kin contact', widget=forms.TextInput(attrs={'placeholder': 'Enter contact of next of kin'}))
    gender = forms.ChoiceField(widget=forms.Select, choices=GENDER)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'telephone', 'id_type', 'id_number',
            'date_of_birth', 'gender', 'next_of_kin_name', 'next_of_kin_contact',
            'employer_type', 'organization', 'organization',     
          )
        widgets = {
            'date_of_birth': widgets.DateInput(attrs={'type': 'date'}),
        } 









