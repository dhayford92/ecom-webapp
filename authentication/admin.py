from django.contrib import admin
from . models import*
from django.contrib.auth.admin import UserAdmin as BaseUserAmin

#User admin
class UserAdmin(BaseUserAmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        ( None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
        ),
    )
    list_display = ('email', 'name', 'is_staff', 'is_verify', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verify', 'groups')
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ('groups', 'user_permissions',)

#Profile Admin Panel 
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'number', 'gender', 'dob')
    list_filter = ['gender']
    search_fields = ['number']
    class Meta:
        model = Profile



admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)