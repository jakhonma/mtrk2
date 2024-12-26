from django.contrib import admin
from authentication.models import User, AdminUser, ArchiveDirectorUser, ChannelDirectorUser, ArchiveEmployeeUser, ChannelEmployeeUser, LowUser, UserRoles
from django.utils.translation import gettext_lazy as _
from .models import AdminUser


class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'password', 'email', 'full_name', 'is_active', 'is_staff', 'date_joined', 'role')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:
            form.base_fields['role'].initial = 'ADMIN'
        return form


admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register([User, ArchiveDirectorUser, ChannelDirectorUser, ArchiveEmployeeUser, ChannelEmployeeUser, LowUser, UserRoles])
