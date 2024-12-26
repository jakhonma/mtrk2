from django.contrib import admin
from django.contrib.auth.models import Permission
from controller.models import Channel, Archive

admin.site.register([Channel, Archive, Permission])
