from django.db import models
from django.core.exceptions import ValidationError
from utils.directory import directory_path


class Poster(models.Model):
    objects = models.Manager()
    image = models.ImageField(upload_to=directory_path, blank=True, null=True)

    def clean(self):
        MAX_SIZE = 1024*1024
        MIN_SIZE = 1024
        image_size = self.image.size
        width, height = self.image.width, self.image.height
        if image_size >= MAX_SIZE:
            raise ValidationError("1 Mbdan kichikroq rasm kiriting")
        if image_size < MIN_SIZE:
            raise ValidationError("1 Kbdan katta rasm kiriting")
        if width > height:
            raise ValidationError("Poster uchun o'lcham notug'ri(160X230)")
        return self

    def __str__(self):
        return f"poster -> {self.pk}"
