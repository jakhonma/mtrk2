from django.core.exceptions import ValidationError
from django.db import models
from helper.models import AbstractClass, Fond


class Category(AbstractClass):
    fond = models.ForeignKey(
        Fond,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True,
        blank=True
    )
    parent = models.ForeignKey(
        'self',
        related_name='children',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    def clean(self):
        if self.fond is not None and self.parent is not None:
            raise ValidationError("Fond va Parent qushish mumkin emas")
        if self.parent is None and self.fond is None:
            raise ValidationError("Fond or Parent is None")
        if self.parent is not None and self.parent.name == self.name:
            raise ValidationError("Parent name mustn't be same")

    def __str__(self):
        return f"{self.name} -> {self.fond}"