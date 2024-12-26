from django.db import models


class Sender(models.Model):
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.name
