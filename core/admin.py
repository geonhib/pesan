from django.contrib import admin
from .models import Package, Sacco, License, SaccoUser, Trail


admin.site.register(Package)
admin.site.register(Sacco)
admin.site.register(SaccoUser)
admin.site.register(Trail)

@admin.register(License)
class UserAdmin(admin.ModelAdmin):
    list_display = ['sacco', 'expiry_date' ]
    readonly_fields = ['key', ]
