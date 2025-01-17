from django.contrib import admin
from letter.models import Letter, LetterProgress

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['pk', 'start_date', 'updated']

admin.site.register(LetterProgress)
