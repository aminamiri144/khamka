from django.contrib import admin

from requisitions.models import Request, Survey, Category, Attachment


class RequestAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'status')


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('request', 'customer', 'date', 'score')
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category_type', 'description')
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('request', 'name', 'filename', 'register_date')


admin.site.register(Request, RequestAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Attachment, AttachmentAdmin)
