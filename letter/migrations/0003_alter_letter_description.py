# Generated by Django 5.0.7 on 2025-01-03 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0002_alter_letter_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='description',
            field=models.CharField(max_length=800),
        ),
    ]
