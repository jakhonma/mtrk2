# Generated by Django 5.0.7 on 2024-12-26 09:27

import django.core.validators
import django.db.models.deletion
import utils.directory
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('helper', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=utils.directory.directory_path)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('mtv_index', models.CharField(blank=True, max_length=100, null=True)),
                ('location_on_server', models.CharField(blank=True, max_length=200, null=True)),
                ('color', models.CharField(choices=[('coloured', 'coloured'), ('white-black', 'white-black')], default='coloured', max_length=12)),
                ('material', models.CharField(choices=[('ether', 'ether'), ('primary', 'primary')], default='ether', max_length=10)),
                ('duration', models.TimeField(blank=True, null=True)),
                ('year', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1920, message="Yilni tug'ri kiriting?"), django.core.validators.MaxValueValidator(2024, message="Yilni tug'ri kiriting?")])),
                ('month', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1, message="Oyni tug'ri kiriting?"), django.core.validators.MaxValueValidator(12, message="Oyni tug'ri kiriting?")])),
                ('day', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1, message="Kunni tug'ri kiriting?"), django.core.validators.MaxValueValidator(31, message="Kunni tug'ri kiriting?")])),
                ('restorat', models.CharField(blank=True, max_length=200, null=True)),
                ('restoration', models.BooleanField(default=False)),
                ('confidential', models.BooleanField(default=False)),
                ('brief_data', models.TextField(blank=True, db_index=True, null=True)),
                ('summary', models.TextField(blank=True, db_index=True, null=True)),
                ('is_serial', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='helper.category')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('fond', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='helper.fond')),
                ('format', models.ManyToManyField(blank=True, related_name='format', to='helper.format')),
                ('language', models.ManyToManyField(blank=True, related_name='language', to='helper.language')),
                ('mtv', models.ManyToManyField(blank=True, related_name='mtv', to='helper.mtv')),
                ('region', models.ManyToManyField(blank=True, related_name='region', to='helper.region')),
                ('poster', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.poster')),
            ],
            options={
                'permissions': [('can_confidential', 'Can confidential information')],
            },
        ),
        migrations.CreateModel(
            name='Cadre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=utils.directory.directory_path)),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='information', to='main.information')),
            ],
        ),
        migrations.CreateModel(
            name='Serial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part', models.PositiveSmallIntegerField()),
                ('duration', models.TimeField()),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serials', to='main.information')),
            ],
            options={
                'ordering': ['part'],
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
                ('information', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rel_information', to='main.information')),
            ],
            options={
                'unique_together': {('user', 'information')},
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='main.information')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'information')},
            },
        ),
        migrations.AddConstraint(
            model_name='serial',
            constraint=models.UniqueConstraint(fields=('information', 'part'), name='unique appversion'),
        ),
    ]
