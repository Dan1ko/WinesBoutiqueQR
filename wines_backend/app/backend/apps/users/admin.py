from . models import User
from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id', 'username', 'created_at')


admin.site.register(User, UserAdmin)
