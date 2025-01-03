# Generated by Django 5.0.7 on 2025-01-03 04:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1920, message="Yilni tug'ri kiriting?"), django.core.validators.MaxValueValidator(2025, message="Yilni tug'ri kiriting?")]),
        ),
    ]