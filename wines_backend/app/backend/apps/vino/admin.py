from backend.apps.vino.models import Wine
from parler.admin import TranslatableAdmin
from django.contrib import admin


class WineAdmin(TranslatableAdmin):

    list_display = ('id', 'image', 'name', 'description', 'price', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('image', 'name', 'description', 'price'),
        }),
    )


admin.site.register(Wine, WineAdmin)
