# Generated by Django 3.1.4 on 2020-12-29 12:41

import backend.apps.horeca.models
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vino', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horeca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=backend.apps.horeca.models.Horeca.upload_to)),
                ('qr', models.ImageField(blank=True, null=True, upload_to='qr_codes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Horeca',
                'verbose_name_plural': 'Horecas',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='HorecaWine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('horeca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wine_horeca', to='horeca.horeca')),
                ('wine', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='horeca_wine', to='vino.wine')),
            ],
            options={
                'verbose_name': 'HorecaWine',
                'verbose_name_plural': 'HorecaWines',
            },
        ),
        migrations.AddField(
            model_name='horeca',
            name='wines',
            field=models.ManyToManyField(blank=True, related_name='wines', through='horeca.HorecaWine', to='vino.Wine'),
        ),
        migrations.CreateModel(
            name='HorecaTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Horeca name')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='horeca.horeca')),
            ],
            options={
                'verbose_name': 'Horeca Translation',
                'db_table': 'horeca_horeca_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]