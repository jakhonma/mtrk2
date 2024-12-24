from django.db import models


class AbstractClass(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
