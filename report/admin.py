from django.contrib import admin
from report.models import Report, InfoItem

admin.site.register([Report, InfoItem])
