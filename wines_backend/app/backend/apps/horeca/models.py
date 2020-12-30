from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import ugettext_lazy as _
from backend.apps.vino.models import Wine
from django.utils import timezone
from django.db import models
import os
import re


class HorecaWine(models.Model):
    horeca = models.ForeignKey('Horeca', related_name='wine_horeca', on_delete=models.CASCADE, blank=True, null=True)
    wine = models.ForeignKey(Wine, related_name='horeca_wine', on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("HorecaWine")
        verbose_name_plural = _("HorecaWines")


class Horeca(TranslatableModel):
    def upload_to(self, filename):
        ext = filename.split('.')[-1]
        name = re.sub(r'\s+|\W+', '_', filename.split('.')[-2])
        file = f'{name}.{ext}'
        today = timezone.now().date()
        return os.path.join('horeca', today.strftime('%d-%m-%Y'), file)

    def qr_to(self, filename):
        ext = filename.split('.')[-1]
        name = re.sub(r'\s+|\W+', '_', filename.split('.')[-2])
        file = f'{name}.{ext}'
        today = timezone.now().date()
        return os.path.join('qr_codes', today.strftime('%d-%m-%Y'), file)

    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    wines = models.ManyToManyField(Wine, related_name='wines', through=HorecaWine, blank=True)
    qr = models.ImageField(upload_to=qr_to, null=True, blank=True)
    translations = TranslatedFields(
        name=models.CharField(_("Horeca name"), max_length=200, null=True, blank=True),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Horeca")
        verbose_name_plural = _("Horecas")

    # def get_url(self):
    #     return f'https://www.pereto.ml/api/horeca/{self.id}/'

    def __str__(self):
        return self.name
