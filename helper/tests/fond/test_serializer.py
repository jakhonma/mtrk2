from django.test import TestCase
from helper.serializers import Fond, Department
from helper.serializers import FondSerializer
from django.forms.models import model_to_dict


class TestFondSerializer(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="mtrk")
        self.fond = Fond.objects.create(department=self.department, name="Kino")

    def test_data(self):
        data = FondSerializer(instance=self.fond).data
        assert data['id'] == self.fond.id
        assert data['name'] == self.fond.name
        assert data['department'] == model_to_dict(self.fond.department)
