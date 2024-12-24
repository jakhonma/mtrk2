from rest_framework import generics, response, permissions
from helper.models import Mtv, Format, Language, Region
from helper.serializers import (
    MtvSerializer,
    FormatSerializer,
    LanguageSerializer,
    RegionSerializer
)
from helper.views import AbstractClassViewSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from helper.serializers import HelperListSerializer


class MTVViewSet(AbstractClassViewSet):
    queryset = Mtv.objects.all()
    serializer_class = MtvSerializer


class FormatViewSet(AbstractClassViewSet):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer


class LanguageViewSet(AbstractClassViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class RegionViewSet(AbstractClassViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class HelperListView(generics.ListAPIView):
    """
        Mtv, Region, Language va Format Listni qaytaradigan View
    """
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 5))
    def list(self, request, *args, **kwargs):
        mtvs = Mtv.objects.all()
        regions = Region.objects.all()
        languages = Language.objects.all()
        formats = Format.objects.all()

        data = {
            "mtvs": MtvSerializer(mtvs, many=True).data,
            "regions": RegionSerializer(regions, many=True).data,
            "languages": LanguageSerializer(languages, many=True).data,
            "formats": FormatSerializer(formats, many=True).data,
        }

        helpers = HelperListSerializer(data)

        return response.Response(helpers.data)
