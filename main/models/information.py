from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class Information(models.Model):
    class Colors(models.TextChoices):
        COLOURED = 'coloured', 'coloured'
        WHITE_BLACK = 'white-black', 'white-black'

    class Material(models.TextChoices):
        ETHER = 'ether', 'ether'
        PRIMARY = 'primary', 'primary'

    employee = models.ForeignKey(
        'authentication.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    fond = models.ForeignKey(
        'helper.Fond',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        'helper.Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    mtv = models.ManyToManyField(
        'helper.Mtv',
        related_name='mtv',
        blank=True
    )
    region = models.ManyToManyField(
        'helper.Region',
        related_name='region',
        blank=True
    )
    language = models.ManyToManyField(
        'helper.Language',
        related_name='language',
        blank=True
    )
    format = models.ManyToManyField(
        'helper.Format',
        related_name='format',
        blank=True
    )
    poster = models.OneToOneField(
        'main.Poster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    title = models.CharField(
        max_length=255, 
        db_index=True
    )
    mtv_index = models.CharField(max_length=100, null=True, blank=True)
    location_on_server = models.CharField(max_length=200, null=True, blank=True)
    color = models.CharField(
        max_length=12,
        choices=Colors.choices,
        default=Colors.COLOURED
    )
    material = models.CharField(
        max_length=10,
        choices=Material.choices,
        default=Material.ETHER
    )
    duration = models.TimeField(blank=True, null=True)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1920, message="Yilni tug'ri kiriting?"),
            MaxValueValidator(int(date.today().year), message="Yilni tug'ri kiriting?")
        ],
        null=True,
        blank=True
    )
    month = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, message="Oyni tug'ri kiriting?"),
            MaxValueValidator(12, message="Oyni tug'ri kiriting?")
        ],
        null=True,
        blank=True
    )
    day = models.PositiveIntegerField(null=True, blank=True, validators=[
        MinValueValidator(1, message="Kunni tug'ri kiriting?"),
        MaxValueValidator(31, message="Kunni tug'ri kiriting?")
    ])
    restorat = models.CharField(max_length=200, null=True, blank=True)
    restoration = models.BooleanField(default=False)
    confidential = models.BooleanField(default=False)
    brief_data = models.TextField(null=True, blank=True, db_index=True)
    summary = models.TextField(null=True, blank=True, db_index=True)
    is_serial = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = [
            ('can_confidential', 'Can confidential information'),
        ]

    def __str__(self):
        return self.title
