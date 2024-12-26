# Generated by Django 5.0.7 on 2024-12-26 09:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_archive_director', to='authentication.archivedirectoruser')),
                ('employee', models.ManyToManyField(blank=True, related_name='rel_archive_employeis', to='authentication.archiveemployeeuser')),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=13)),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_channel_director', to='authentication.channeldirectoruser')),
                ('employee', models.ManyToManyField(blank=True, related_name='rel_channel_employeis', to='authentication.channelemployeeuser')),
            ],
        ),
    ]
