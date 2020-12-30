from backend.apps.horeca.models import Horeca
from parler.admin import TranslatableAdmin
from django.contrib import admin


class WinesInline(admin.TabularInline):
    model = Horeca.wines.through


class HorecaAdmin(TranslatableAdmin):

    def wines_display(self, obj):
        return ", ".join([
            wine.name for wine in obj.wines.all()
        ])

    wines_display.short_description = "Wines"

    list_display = ('id', 'image', 'name', 'qr', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('image', 'name', 'qr'),
        }),
    )

    inlines = (WinesInline,)


admin.site.register(Horeca, HorecaAdmin)
