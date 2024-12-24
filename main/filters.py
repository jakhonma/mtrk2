from django_filters import rest_framework as filters
from .models import Information
from django.db.models import Q


class InformationFilter(filters.FilterSet):
    fond = filters.BaseInFilter(
        field_name='fond__id',
        lookup_expr='in'
    )
    parents = filters.BaseInFilter(
        field_name='category__parent__id',
        lookup_expr='in',
        method='filter_parents_or_categories'
    )
    categories = filters.BaseInFilter(
        field_name='category__id', 
        lookup_expr='in'
    )
    fond__department__name = filters.CharFilter(
        field_name='fond__department__name', 
        lookup_expr='icontains'
    )
    region = filters.BaseInFilter(
        field_name='region__id', 
        lookup_expr='in'
    )
    is_serial = filters.BooleanFilter(
        field_name='is_serial'
    )
    year = filters.RangeFilter(
        field_name='year'
    )

    class Meta:
        model = Information
        fields = ['fond__department__name', 'fond', 'parents', 'categories', 'year', 'region', 'is_serial']

    def filter_parents_or_categories(self, queryset, name, value):
        """
            Agar parents mavjud bo'lsa, parent orqali, bo'lmasa category orqali filter.
        """
        queryset = queryset.filter(Q(category__parent__id__in=value) | Q(category__id__in=value)).distinct()
        return queryset
