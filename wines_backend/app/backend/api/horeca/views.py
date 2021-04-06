from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files.base import File
from backend.apps.horeca.models import Horeca, HorecaWine
from backend.api.horeca.serializers import HorecaSerializer, HorecaListSerializer, HorecaUpdateSerializer
from backend.apps.wine.models import Wine
from backend.utils import CustomJsonRenderer, StandardSetPagination
from drf_nested_multipart_parser import NestedMultipartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from backend.api.permissions import IsAdmin
import qrcode
import re


class HorecaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin, )
    renderer_classes = (CustomJsonRenderer,)
    queryset = Horeca.objects.all()
    serializer_class = HorecaSerializer
    pagination_class = StandardSetPagination
    parser_classes = (JSONParser, NestedMultipartParser)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['translations__name']
    search_fields = ['translations__name']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        horeca = serializer.save()
        arr_wine = []
        for key in request.data.keys():
            match = re.match(r'(wines)_(\d)', key)
            if match:
                arr_wine.append(int(request.data[key]))
        horeca.save()
        for wine_id in arr_wine:
            horeca.wines.add(Wine.objects.get(id=wine_id))
        img = qrcode.make('www.google.com')
        canvas = Image.new('RGB', (300, 300), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(img)
        blob = BytesIO()
        canvas.save(blob, 'PNG')
        horeca.qr.save('qr_code.png', File(blob), save=False)
        horeca.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # instance.wines.clear()
        # instance.save()
        arr_wine = []
        for key in request.data.keys():
            match = re.match(r'(wines)_(\d)', key)
            if match:
                arr_wine.append(int(request.data[key]))
        instance.save()
        for resource_id in arr_wine:
            instance.resources.add(Wine.objects.get(id=resource_id))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HorecaListViewSet(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    renderer_classes = (CustomJsonRenderer,)
    queryset = Horeca.objects.all()
    serializer_class = HorecaListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['translations__name']
    search_fields = ['translations__name']

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            serializer = self.get_serializer(Horeca.objects.get(id=kwargs['pk']))
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)


class HorecaUpdateViewSet(generics.UpdateAPIView):
    permission_classes = (IsAdmin, )
    renderer_classes = (CustomJsonRenderer,)
    queryset = Horeca.objects.all()
    serializer_class = HorecaUpdateSerializer


class HorecaWineDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdmin,)
    renderer_classes = (CustomJsonRenderer,)
    queryset = Wine.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        horeca = kwargs.get('horeca_id', None)
        if horeca:
            resource = HorecaWine.objects.filter(horeca__id=horeca, wine_id=instance.id)
            resource.delete()
        return Response("Article's resource is deleted")
