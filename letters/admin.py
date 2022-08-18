from django.contrib import admin
from letters.models import Letter


class LetterAdmin(admin.ModelAdmin):
    list_display = ('letter_number', 'title', 'recepiant', 'status')
# Register your models here.

admin.site.register(Letter, LetterAdmin)
# Register your models here.
