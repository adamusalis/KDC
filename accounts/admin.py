from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # This dictates how the list of users looks
    list_display = ('phone_number', 'email', 'wallet_balance', 'is_staff')
    ordering = ('phone_number',)
    search_fields = ('phone_number', 'email')

    # This dictates what fields you see when you click on a user
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('VTU Wallet', {'fields': ('wallet_balance', 'transaction_pin')}), # <--- Your custom fields
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
   
    # This dictates the "Add User" form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password'),
        }),
    )

# Register the new setup
admin.site.register(CustomUser, CustomUserAdmin)