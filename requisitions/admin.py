from django.contrib import admin

from requisitions.models import Request, Survey


class RequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'status')

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('request', 'customer', 'date', 'score')
# Register your models here.

admin.site.register(Request, RequestAdmin)
admin.site.register(Survey, SurveyAdmin)
