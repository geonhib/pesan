from django import forms
from .models import Sacco, Package, License
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets


class SaccoForm(forms.ModelForm):    
    package = forms.ModelChoiceField(queryset=Package.objects.filter(status='active'), empty_label='Select business package')
    name = forms.CharField(label='Name of business', widget=forms.TextInput(attrs={'placeholder': 'Enter name of business'}))
    district = forms.CharField(label='District', widget=forms.TextInput(attrs={'placeholder': 'Enter district of business location'}))
    location = forms.CharField(label='Location', widget=forms.TextInput(attrs={'placeholder': 'Enter physical address'}))
    email = forms.CharField(label='Email address', widget=forms.TextInput(attrs={'placeholder': 'Enter email address'}))
    telephone = forms.CharField(label='Telephone', widget=forms.TextInput(attrs={'placeholder': 'Enter telephone number'}))

    class Meta:
        model = Sacco
        fields = ('name', 'package', 'district', 'location', 'email', 'telephone',   )


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'capacity', 'status']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['email', 'gender', ]


class LicenseForm(forms.ModelForm):
    business = forms.ModelChoiceField(queryset=Sacco.objects.filter(status='inactive'), label='Sacco', empty_label='Select sacco')
    class Meta:
        model = License
        fields = [ 'business', 'expiry_date', ]
        widgets = {
            'expiry_date': widgets.DateInput(attrs={'type': 'date'}),
        }

    def __int__(self, *args, **kwargs):
        super(LicenseForm, self).__init__(*args, **kwargs)
        self.fields['key'].widget.attrs['readonly'] = True

    # def clean(self):
    #     x = ''
    #     return x
