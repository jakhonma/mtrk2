from helper.models import Department
from helper.serializers import DepartmentSerializer
from helper.views import AbstractClassViewSet


class DepartmentViewSet(AbstractClassViewSet):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()
