from backend.utils import CustomJsonRenderer, StandardSetPagination
from backend.api.wine.serializers import WineSerializer, WineListSerializer
from backend.apps.wine.models import Wine
from drf_nested_multipart_parser import NestedMultipartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from backend.api.permissions import IsAdmin


class WineViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    renderer_classes = (CustomJsonRenderer,)
    queryset = Wine.objects.all()
    serializer_class = WineSerializer
    pagination_class = StandardSetPagination
    parser_classes = (JSONParser, NestedMultipartParser)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['translations__name']
    search_fields = ['translations__name']


class WineListViewSet(generics.ListAPIView):
    permission_classes = (IsAdmin,)
    renderer_classes = (CustomJsonRenderer,)
    queryset = Wine.objects.all()
    serializer_class = WineListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['translations__name']
    search_fields = ['translations__name']

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            serializer = self.get_serializer(Wine.objects.get(id=kwargs['pk']))
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
