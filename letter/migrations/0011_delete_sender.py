# Generated by Django 5.0.7 on 2025-01-14 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0010_remove_letter_current_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sender',
        ),
    ]
