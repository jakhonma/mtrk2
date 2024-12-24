from django.db import models
from authentication.models import User
from main.models import Information
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    information = models.ForeignKey(Information, on_delete=models.CASCADE, related_name="ratings")
    rating = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'information')

    def __str__(self):
        return f'{self.user} - {self.information}'
