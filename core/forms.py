from django import forms
from .models import Sacco, Package, License
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets



SACCO_TYPE = (
    ('savings', 'savings'),
    ('loans', 'loans')
)
class SaccoForm(forms.ModelForm):   
    type = forms.ChoiceField(label='Sacco type', widget=forms.Select, choices=SACCO_TYPE)
    tin = forms.CharField(label='Tax Indentification Number', widget=forms.TextInput(attrs={'placeholder': 'Enter your TIN'}))
    package = forms.ModelChoiceField(queryset=Package.objects.filter(status='active'), empty_label='Select business package')
    name = forms.CharField(label='Name of business', widget=forms.TextInput(attrs={'placeholder': 'Enter name of business'}))
    district = forms.CharField(label='District', widget=forms.TextInput(attrs={'placeholder': 'Enter district of business location'}))
    location = forms.CharField(label='Office location', widget=forms.TextInput(attrs={'placeholder': 'Enter physical address'}))
    email = forms.CharField(label='Email address', widget=forms.TextInput(attrs={'placeholder': 'Enter email address of sacco'}))

    class Meta:
        model = Sacco
        fields = (
            'name', 'type', 'tin', 'package', 'district', 'location', 'email', 'incorporation',
            'permit',  'by_laws', 'recommendation', 
          )


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name', 'capacity', 'price', ]



class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['email', 'gender', ]


class LicenseForm(forms.ModelForm):
    sacco = forms.ModelChoiceField(queryset=Sacco.objects.filter(status='inactive'), label='Sacco', empty_label='Select sacco')
    class Meta:
        model = License
        fields = [ 'sacco', 'expiry_date', ]
        widgets = {
            'expiry_date': widgets.DateInput(attrs={'type': 'date'}),
        }

    def __int__(self, *args, **kwargs):
        super(LicenseForm, self).__init__(*args, **kwargs)
        self.fields['key'].widget.attrs['readonly'] = True

    


