from django.contrib import admin
from letter.models import Letter, Notification, LetterProgress, Sender

admin.site.register([Letter, Notification, LetterProgress, Sender])
