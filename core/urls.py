from audioop import lin2adpcm
from django.urls import path
from .views import (
    settings, Homepage, dashboard, 
    sacco_add, SaccoListView, 
    SaccoDetailView, SaccoDeleteView,  SaccoUpdateView, 
    sacco_activation, 
    PackageListView, PackageDetailView, 
    PackageUpdateView, PackageCreateView, PackageDeleteView, 
    package_activation, register,
    LicenseCreateView, LicenseListView, LicenseUpdateView, LicenseDeleteView,
    # license_add, 

)

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('dashboard', dashboard, name='dashboard'),
    path('settings', settings, name='settings'),

    path('packages/add', PackageCreateView.as_view(), name='package_add' ),
    path('packages', PackageListView.as_view(), name='package_list'),
    path('packages/<int:pk>/detail', PackageDetailView.as_view(), name='package_detail'),
    path('packages/<int:pk>/update', PackageUpdateView.as_view(), name='package_update'),
    path('packages/<str:pk>/delete', PackageDeleteView.as_view(), name='package_delete'),   
    path('package_activation/<str:pk>', package_activation, name='package_activation'),  

    path('saccos/add', sacco_add, name='sacco_add' ),
    path('saccos', SaccoListView.as_view(), name='sacco_list'),
    path('saccos/<str:pk>/detail', SaccoDetailView.as_view() , name='sacco_detail'),
    path('saccos/<str:pk>/update', SaccoUpdateView.as_view(), name='sacco_update'),
    path('saccos/<str:pk>/delete', SaccoDeleteView.as_view(), name='sacco_delete'),
    path('saccos_activation/<str:pk>', sacco_activation, name='sacco_activation'),
    # Register user to sacco
    path('register', register, name='register'),

    path('licenses/add', LicenseCreateView.as_view(), name='license_add'),
    path('licenses', LicenseListView.as_view(), name='license_list'),
    # path('licenses/add', license_add, name='license_add'),
    path('licenses/<int:pk>/update', LicenseUpdateView.as_view(), name='license_update'),
    path('licenses/<str:pk>/delete', LicenseDeleteView.as_view(), name='license_delete'), 

]