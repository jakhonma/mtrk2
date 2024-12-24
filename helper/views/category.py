from rest_framework import viewsets, generics, permissions
from helper.models import Category
from helper.serializers import (
    CategorySerializer,
    NestedCategorySerializer,
    InformationCategorySerializer
)


class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(fond__isnull=False)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = NestedCategorySerializer


class CategoryFondListView(generics.ListAPIView):
    """
        Fondga tegishli Categorylarni qaytaradigan View
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InformationCategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(
            fond_id=self.kwargs['fond_id'],
            fond__isnull=False
        )
        return queryset


class ParentCategoryListView(generics.ListAPIView):
    """
        Parentga tegishli Categorylarni qaytaradigan View
    """
    serializer_class = InformationCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Category.objects.filter(
            parent_id=self.kwargs['category_id'],
            fond__isnull=True
        )
        return queryset


#Filter
class CategoryFondIdListView(generics.ListAPIView):
    """
        Fond Id Listga tegishli Categorylarni qaytaradigan View
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InformationCategorySerializer

    def get_queryset(self):
        fond_id_list = self.request.query_params.getlist('fonds')
        if fond_id_list:
            queryset = Category.objects.filter(
                fond__id__in=fond_id_list,
                fond__isnull=False
            )
        else:
            queryset = Category.objects.filter(
                fond__isnull=False
            )
        return queryset


class CategoryParenIdListView(generics.ListAPIView):
    """
        Parent Id Listga tegishli Categorylarni qaytaradigan View
    """
    serializer_class = InformationCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        parent_list_id = self.request.query_params.getlist('parents')
        if parent_list_id:
            queryset = Category.objects.filter(
                parent__id__in=parent_list_id,
                fond__isnull=True
            )
        else:
            queryset = Category.objects.filter(
                fond__isnull=True
            )
        return queryset
