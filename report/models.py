from django.db import models


class Report(models.Model):
    fond = models.ForeignKey(
        'helper.Fond',
        on_delete=models.SET_NULL,
        null=True
    )
    send_mtv = models.ForeignKey(
        'helper.Mtv',
        on_delete=models.SET_NULL,
        related_name='send_mtv',
        null=True
    )
    received_mtv = models.ForeignKey(
        'helper.Mtv',
        on_delete=models.SET_NULL,
        related_name='received_mtv',
        null=True
    )
    employee = models.ForeignKey(
        'authentication.ArchiveEmployeeUser',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    number = models.PositiveSmallIntegerField(default=0)
    dvd_number = models.PositiveSmallIntegerField(default=0)
    info = models.CharField(max_length=455, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.info[:100]


class InfoItem(models.Model):
    report = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        related_name="reports"
    )
    name = models.CharField(max_length=255)
    duration = models.TimeField()

    def __str__(self):
        return self.name
