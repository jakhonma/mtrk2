# Generated by Django 5.0.7 on 2025-01-16 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0011_delete_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
