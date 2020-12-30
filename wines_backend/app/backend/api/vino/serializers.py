from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from backend.mixins import TranslatedSerializerMixin
from backend.apps.vino.models import Wine
from rest_framework import serializers


class WineSerializer(TranslatedSerializerMixin, TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Wine, required=False)

    class Meta:
        model = Wine
        fields = '__all__'
        read_only_fields = ('id',)


class WineListSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Wine, required=False)

    class Meta:
        model = Wine
        fields = '__all__'
