from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea

from .models import User


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'username', 'first_name',)
    fieldsets = (
        (None,
         {'fields': (
             'email', 'username', 'first_name', 'last_name', 'role')}),
        ('Personal', {'fields': ('bio',)}),
    )
    formfield_overrides = {
        User.bio: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


admin.site.register(User, UserAdminConfig)
