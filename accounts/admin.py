from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserChangeForm
# Register your models here.
admin.site.register(User, UserAdmin)

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)