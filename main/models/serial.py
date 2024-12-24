from django.db import models


class Serial(models.Model):
    information = models.ForeignKey(
        'main.Information',
        on_delete=models.CASCADE,
        related_name='serials'
    )
    part = models.PositiveSmallIntegerField()
    duration = models.TimeField()

    class Meta:
        ordering = ['part']
        constraints = [
            models.UniqueConstraint(
                fields=['information', 'part'],
                name='unique appversion'
            )
        ]

    def __str__(self):
        return self.information.title
