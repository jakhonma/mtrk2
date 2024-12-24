from django.test import TestCase
from helper.serializers import Department
from helper.serializers import DepartmentSerializer


class TestDepartmentSerializerTestCase(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Department")

    def test_data(self):
        data = DepartmentSerializer(instance=self.department).data
        assert data['id'] == self.department.id
        assert data['name'] == self.department.name

    def test_unique_name_constraint(self) -> None:
        data = {
            "name": "Department"
        }
        serializer = DepartmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        self.assertEqual(serializer.errors['name'][0], "Department with this name already exists.")
