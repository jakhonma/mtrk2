from django.db import models
from helper.models import AbstractClass, Department


class Fond(AbstractClass):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='fonds'
    )

    def __str__(self):
        return f"{self.name} {self.department.name}"