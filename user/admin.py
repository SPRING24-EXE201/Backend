from django.contrib import admin

from user.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'full_name', 'phone_number', 'address', 'image_link')