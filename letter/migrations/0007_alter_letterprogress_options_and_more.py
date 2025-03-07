# Generated by Django 5.0.7 on 2025-01-13 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letter', '0006_alter_letterprogress_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='letterprogress',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='letterprogress',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
