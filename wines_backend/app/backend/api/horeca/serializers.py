from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from backend.mixins import TranslatedSerializerMixin
from backend.api.vino.serializers import *
from backend.apps.horeca.models import Horeca
from rest_framework import serializers


class HorecaSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Horeca, required=False)
    wines = WineSerializer(many=True, read_only=True)

    class Meta:
        model = Horeca
        fields = ('id', 'image', 'translations', 'wines', 'qr', 'created_at')
        read_only_fields = ('id',)


class HorecaUpdateSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Horeca, required=False)
    wines = WineSerializer(many=True, read_only=True)

    class Meta:
        model = Horeca
        fields = ('id', 'image', 'translations', 'wines', 'qr', 'created_at')
        read_only_fields = ('id',)


class HorecaListSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Horeca, required=False)
    wines = WineSerializer(many=True, read_only=True)

    class Meta:
        model = Horeca
        fields = '__all__'
