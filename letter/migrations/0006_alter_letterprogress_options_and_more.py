# Generated by Django 5.0.7 on 2025-01-10 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0005_alter_letterprogress_sent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letterprogress',
            options={'ordering': ['-updated']},
        ),
        migrations.RemoveField(
            model_name='letterprogress',
            name='status',
        ),
    ]
