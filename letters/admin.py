from django.contrib import admin
from letters.models import Letter, Organ


class LetterAdmin(admin.ModelAdmin):
    list_display = ('letter_number', 'title', 'recepiant', 'status')
# Register your models here.

class OrganAdmin(admin.ModelAdmin):
    list_display = ('name', 'org_type', 'decriptions')


admin.site.register(Letter, LetterAdmin)
admin.site.register(Organ, OrganAdmin)
# Register your models here.
