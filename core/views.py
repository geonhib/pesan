from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from accounts.decorators import user_logged_in_before
from django.contrib.auth.decorators import login_required
import urllib.request
from django.utils import timezone
from django.contrib import messages
from core.forms import SaccoForm, LicenseForm
from .models import Sacco, SaccoUser, Package, License, Trail
from django.contrib.auth import get_user_model
User = get_user_model()
from accounts.forms import UserForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.conf import settings
host = settings.EMAIL_HOST_USER
from django.db import models
from .forms import PackageForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group


def error_404(request, exception):
    data = {}
    return render(request, '400.html', status=404)


def error_500(request):
    data = {}
    return render(request, '500.html', status=500)


class Waiting(TemplateView):
    template_name = 'inactive_sacco.html'


class EmailThread(threading.Thread):
    """
    Threaded object to handle sending emails asynchronously
    """
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list, self.fail_silently, self.html)
        if self.html:
            msg.attach_alternative(self.html, 'text/html')
        msg.send(self.fail_silently)

    def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
        try:
            urllib.request.urlopen(host='http://google.com', timeout=4)
            EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()
        except:
            print('Sorry there is no internet connection')


class Homepage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return super().get(request, *args, **kwargs)



@login_required
@user_logged_in_before
def dashboard(request):
    if request.user.is_superuser:
        saccos = Sacco.objects.all()
        trails = Trail.objects.all()
        sacco_user = ''
        sacco = ''
        
    else:
        saccos = ''
        sacco_user = SaccoUser.objects.get(user=request.user)
        sacco=sacco_user.sacco
        sacco_status=sacco_user.sacco.status

        if sacco_status == 'inactive':
            return redirect('waiting')
        else:
            trails = Trail.objects.filter(sacco=sacco)
            print(trails)
    context = {
        'saccos': saccos,
        'trails': trails[:4],
        'sacco': sacco,
        }
    return render(request, 'dashboard.html', context)


def settings(request):
    return render(request, 'settings.html')


class SaccoListView(ListView):
    model = Sacco
    template_name = 'saccos/list.html'
    context_object_name = 'saccos'

    def get_queryset(self):
        groups = Group.objects.all()
        print(groups)
        return super().get_queryset()


def sacco_add(request):
    if request.method == 'POST':
        sacco_form = SaccoForm(request.POST, request.FILES)
        user_form = UserForm(request.POST, request.FILES)
        if sacco_form.is_valid() and user_form.is_valid():
            sacco_instance = sacco_form.save(commit=False)
            user_instance = user_form.save(commit=False)
            user_instance.is_staff = True
            password = User.objects.make_random_password()
            user_instance.set_password(password)

            sacco_instance.created_by = request.user
            sacco_instance.created_on = timezone.now()
            sacco_instance.director = user_instance

            if User.objects.filter(email=user_instance.email).exists():
                raise ValidationError('Director already exists')
            else:
                user_instance.save()
                user_instance = authenticate(email=user_instance.email, password=password)
                sacco_instance.save()
                sacco_user = SaccoUser.objects.create(user=user_instance, sacco=sacco_instance)
                print(f"sacco:{sacco_instance} created for user:{sacco_instance.director} password: {password}")
                msg = f"sacco:{sacco_instance} created for user:{sacco_instance.director}"
                messages.success(request, msg)
                # audit
                email=user_instance.email
                EmailThread.send_mail('School registered', msg, host, [email, ], fail_silently=False)
                return redirect('license_list')
            
        else:
            sacco_msg=sacco_form.errors
            user_msg=user_form.errors
            print(sacco_msg)
            print(user_msg)
            messages.warning(request, sacco_msg)
            messages.warning(request, user_msg)
            raise ValidationError('Sorry, sacco could not be created.')

    else:
        sacco_form = SaccoForm()
        user_form = UserForm()

    context = {
        'sacco_form': sacco_form,
        'user_form': user_form,
    }
    return render(request, 'saccos/add.html', context)



class SaccoDetailView(DetailView):
    model = Sacco
    template_name = "saccos/detail.html"
    context_object_name = 'sacco'


class SaccoUpdateView(UpdateView):
    model = Sacco 
    context_object_name = 'sacco'
    template_name = 'saccos/update.html'
    fields = ['name', 'package', 'district', 'location', 'email', 'director', 'status', 'created_by']
    success_message = "%(sacco) was edited."

    def form_valid(self, form):
        sacco=form.instance
        sacco.updated_by = self.request.user
        sacco.updated_on = timezone.now()
        msg= f"{sacco} updated successfully."
        print(sacco)
        messages.success(self.request, msg)
        Trail.objects.create(sacco=sacco, event=msg, created_on=timezone.now())
        return super().form_valid(form)


class SaccoDeleteView(DeleteView):
    model = Sacco
    # context_object_name = 'sacco'
    template_name = 'delete_template.html'
    success_url = reverse_lazy('sacco_list')

    def form_valid(self, form):
        msg= f"Sacco {form.instance.name} deleted."
        messages.success(self.request, msg)
        return super().form_valid(form)


def sacco_activation(request, pk):
    sacco = get_object_or_404(Sacco, pk=pk)
    activate_msg = f"{request.user} has activated {sacco.name}"
    deactivate_msg = f"{request.user} has suspended {sacco.name}"
    if sacco.status == 'active':
        sacco.status = 'inactive'
        sacco.save()
        messages.info(request, deactivate_msg)
        # Audit.objects.create(event= deactivate_msg, url=request.build_absolute_uri(), created_on=timezone.now(), created_by=request.user)
        return redirect('sacco_detail', sacco.id)
    else: 
        sacco.status = 'active'
        sacco.save()
        messages.info(request, activate_msg)
        # Audit.objects.create(event= activate_msg, url=request.build_absolute_uri(), created_on=timezone.now(), created_by=request.user)
        return redirect('sacco_detail',  sacco.id)


class PackageCreateView(CreateView):
    model = Package
    template_name = "packages/add.html"
    form_class = PackageForm 
    success_url = reverse_lazy('package_list')

    def form_valid(self, form):
        msg= f"Package {{form.instance.name}} created successfully."
        messages.success(self.request, msg)
        return super().form_valid(form)


class PackageListView(ListView):
    model = Package
    context_object_name = 'packages'
    template_name = 'packages/list.html'


class PackageDetailView(DetailView):
    model = Package
    context_object_name = 'package'
    template_name = 'packages/add.html'


class PackageUpdateView(UpdateView):
    model = Package
    context_object_name = 'package'
    template_name = 'packages/add.html'
    form_class = PackageForm
    # pk_url_kwarg: 'id'

    def form_valid(self, form):
        msg= f"Package {{form.instance.name}} updated successfully."
        messages.success(self.request, msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('package_update', kwargs={self.pk_url_kwarg:self.kwargs['pk']})
    

class PackageDeleteView(DeleteView):
    model = Package
    template_name = "delete_template.html"
    context_object_name = 'package'
    success_url = reverse_lazy('package_list')

    def form_valid(self, form):
        msg= f"Package {{form.instance.name}} deleted."
        messages.success(self.request, msg)
        return super().form_valid(form)


def package_activation(request, pk):
    package = get_object_or_404(Package, pk=pk)
    activate_msg = f"{request.user} has activated {package.name}"
    deactivate_msg = f"{request.user} has suspended {package.name}"
    if package.status == 'active':
        package.status = 'inactive'
        package.save()
        messages.info(request, deactivate_msg)
        return redirect('package_list')
    else: 
        package.status = 'active'
        package.save()
        messages.info(request, activate_msg)
        return redirect('package_list')


def member_limit(request):
    """Checks member limit in sacco based on package."""
    sacco = Sacco.objects.get(director=request.user)
    MEMBER_LIMIT = sacco.package.capacity
    sacco_users = SaccoUser.objects.filter(sacco=sacco).select_related('user')
    SACCO_MEMBERS=sacco_users.count()
    if SACCO_MEMBERS <= MEMBER_LIMIT:
        msg='pass'
        print(msg)
        return redirect('register')
    else:
        msg = f"Hi {request.user} your package capacity limit is {MEMBER_LIMIT} and You have reached it"
        messages.info(request, msg)
        return redirect('user_list')
    

@login_required
def register(request):
    """Sacco director adds sacco member"""
    try:
        director = request.user
        sacco = Sacco.objects.get(director=director)
        # sacco_user = SaccoUser.objects.create(user=user, sacco=sacco)
    except:
        sacco_user = ''

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if User.objects.filter(email=user.email).exists():
                messages.info(request, 'User already exists')
                # raise ValidationError('User already exists')
                form = UserForm()
            else:
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                user = authenticate(email=user.email, password=password)  
                sacco_user = SaccoUser.objects.create(user=user, sacco=sacco)
                print(f"Director: {director} created user: {user} password: {password}")
                msg = f"Director: {director} created user: {user}"
                messages.success(request, msg)
                Trail.objects.create(sacco=sacco, event=msg, created_on=timezone.now(), created_by=director)
                email=user.email
                EmailThread.send_mail('School registered', msg, host, [email, ], fail_silently=False)
                SaccoUser.objects.create(user=user, sacco=sacco)
            return redirect('dashboard')
        else:
            print(form.errors)
    else:
        form = UserForm()   
    return render(request, 'account/add.html', {'form': form})


# Generate random string
import random, string
""""Generate license key of comprising of strings, numbers and special characters. """
def generate_license(num=20):
    result=''.join(random.choice(string.ascii_letters) for i in range(num))
    characters = string.ascii_letters + string.digits + string.punctuation
    key = ''.join(random.choice(characters) for i in range(num))
    return key


class LicenseCreateView(CreateView):
    model = License
    template_name = "licenses/add.html"
    form_class = LicenseForm
    success_url = reverse_lazy('license_list')

    def form_valid(self, form):
        sacco_with_active_license = License.objects.filter(sacco=form.instance.sacco, status='active')
        if sacco_with_active_license:
                msg=f"Cannot generate license because {form.instance.sacco} already has an active license"
                messages.info(self.request, msg)
                return redirect('license_add')
        else:
            form.instance.key = generate_license()
            form.instance.sacco.status = 'active'
            form.instance.sacco.save()
            msg=f'License generated for {form.instance.sacco}'
            messages.success(self.request, 'License generated successfuly')
            return super().form_valid(form)


# def license_add(request):
#     if request.method == 'POST':
#         form = LicenseForm(data=request.POST)
    
#         if form.is_valid():
#             instance=form.save(commit=False)
#             sacco = form.cleaned_data['sacco']
#             instance.sacco = sacco
            
#             sacco_with_active_license = License.objects.filter(sacco=sacco, status='active')
#             if sacco_with_active_license:
#                 return redirect('license_add')
#             else:
#                 instance.key=generate_license()
#                 sacco.status = 'active'
#                 sacco.save()
#                 instance.save()
#                 print(f'license {instance.key} added for {instance.sacco}')
#                 return redirect('license_list')
#     else:
#         form = LicenseForm
#     context = {
#         'form': form,
#     }
#     return render(request, 'licenses/add.html', context)

        

class LicenseListView(ListView):
    model = License
    template_name = "licenses/list.html"
    context_object_name = 'licenses'


class LicenseUpdateView(UpdateView):
    model = License
    context_object_name = 'license'
    template_name = 'licenses/add.html'
    form_class = LicenseForm

    def form_valid(self, form):
        msg= f"License key generated for {{form.instance.sacco}}"
        messages.success(self.request, msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('license_update', kwargs={self.pk_url_kwarg:self.kwargs['pk']})


class LicenseDeleteView(DeleteView):
    model = License
    template_name = "delete_template.html"
    context_object_name = 'object'
    success_url = reverse_lazy('license_list')

    def form_valid(self, form):
        msg= f"License key of {{form.instance.sacco}} deleted"
        messages.success(self.request, msg)
        return super().form_valid(form)
    


class ChangePackageView(UpdateView):
    model = Sacco 
    context_object_name = 'sacco'
    template_name = 'packages/change.html'
    fields = [ 'package',]
    success_message = "%(sacco) package was edited."

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        form.instance.updated_on = timezone.now()
        msg= f"Sacco {form.instance.name} updated successfully."
        messages.success(self.request, msg)
        Trail.objects.create(sacco=form.instance, event=msg, created_on=timezone.now())
        return super().form_valid(form)







