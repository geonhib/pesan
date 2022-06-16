from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', ]
    readonly_fields = ['password', 'date_joined', ]
    exclude = ['last_login', ]
    # add_form = UserCreationForm
    # form = UserChangeForm
    # model = User
    # fieldsets = UserAdmin.fieldsets + (
#             ('Extra Fields', {'fields': ('telephone', 'gender', 'photo', 'is_previously_logged_in')}),
#     )