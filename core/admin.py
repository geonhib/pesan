from django.contrib import admin
from .models import Package, Sacco, License


admin.site.register(Package)
admin.site.register(Sacco)


@admin.register(License)
class UserAdmin(admin.ModelAdmin):
    list_display = ['sacco', 'expiry_date' ]
    readonly_fields = ['key', ]
