from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import profile

# Register your models here.


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active','username','first_name','last_name','phone_number')
    list_filter = ('email', 'is_staff', 'is_active','username','first_name','last_name')
    fieldsets = (
        (None, {'fields': ('email', 'password','username','first_name','last_name','phone_number','profile_pic')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','first_name','last_name', 'password1', 'password2','phone_number', 'is_staff', 'is_active',)}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(profile)