from io import BytesIO

import qrcode
from PIL import Image, ImageDraw
from django.core.files import File

from backend.apps.horeca.models import Horeca
from parler.admin import TranslatableAdmin
from django.contrib import admin


class WinesInline(admin.TabularInline):
    model = Horeca.wines.through


class HorecaAdmin(TranslatableAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        img = qrcode.make('www.google.com')
        canvas = Image.new('RGB', (300, 300), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img)
        blob = BytesIO()
        canvas.save(blob, 'PNG')
        obj.qr.save('qr_code.png', File(blob), save=False)
        obj.save()

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
