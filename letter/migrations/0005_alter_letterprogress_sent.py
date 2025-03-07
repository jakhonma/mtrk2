# Generated by Django 5.0.7 on 2025-01-05 09:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0004_rename_timestamp_letterprogress_created_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='letterprogress',
            name='sent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rel_sents', to=settings.AUTH_USER_MODEL),
        ),
    ]
