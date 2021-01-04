from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
import os
import re


class Wine(TranslatableModel):
    def upload_to(self, filename):
        ext = filename.split('.')[-1]
        name = re.sub(r'\s+|\W+', '_', filename.split('.')[-2])
        file = f'{name}.{ext}'
        today = timezone.now().date()
        return os.path.join('wine', today.strftime('%d-%m-%Y'), file)
    price = models.FloatField(default=0.0, blank=True)
    image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    translations = TranslatedFields(
        name=models.CharField(_("Wine name"), max_length=200, null=True, blank=True),
        description=models.TextField(_("Wine description"), blank=True, null=True),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Wine")
        verbose_name_plural = _("Wines")

    # def get_url(self):
    #     return f'https://www.pereto.ml/api/horeca/{self.id}/'

    def __str__(self):
        return self.name
