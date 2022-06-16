from django.urls import path, include
from .views import (
    signup, signin, pre_signout, signout,
    user, user_activation, users, PasswordResetView, password_change,
    first_login,  delete_user,
    )


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('users', users, name='users'),
    path('users/<str:pk>', user, name='user'),
    path('pre_signout', pre_signout, name='pre_signout'),
    path('user_activation/<int:pk>', user_activation, name='user_activation'),
    path('delete_user/<str:pk>', delete_user, name='delete_user'),

    path('first_login', first_login, name='first_login'),
    path('password_reset',PasswordResetView.as_view(), name='password_reset' ),
    path('password_change', password_change, name='password_change'),

    path('accounts/', include('django.contrib.auth.urls')),


    # password_reset [name='reset_password_reset']
    # password_change [name='change_password']
    # accounts/ login/ [name='login']
    # accounts/ logout/ [name='logout']
    # accounts/ password_change/ [name='password_change']
    # accounts/ password_change/done/ [name='password_change_done']
    # accounts/ password_reset/ [name='password_reset']
    # accounts/ password_reset/done/ [name='password_reset_done']
    # accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/ reset/done/ [name='password_reset_complete'] 
    
]