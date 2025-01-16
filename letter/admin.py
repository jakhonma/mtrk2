from django.contrib import admin
from letter.models import Letter, LetterProgress

admin.site.register([Letter, LetterProgress])
