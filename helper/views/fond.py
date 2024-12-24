from rest_framework import generics
from helper.models import Fond
from helper.serializers import FondSerializer
from rest_framework.permissions import IsAuthenticated
from helper.views import AbstractClassViewSet


class FondViewSet(AbstractClassViewSet):
    queryset = Fond.objects.all()
    serializer_class = FondSerializer


class FontListDepartmentAPIView(generics.ListAPIView):
    """
        Bitta Departmentga tegishli Fondlarni qaytaradigan View
    """
    serializer_class = FondSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Fond.objects.filter(
            department_id=self.kwargs['department_id']
        )
        return queryset
