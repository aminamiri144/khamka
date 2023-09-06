from django.contrib import admin

# Register your models here.
from customers.models import Customer, CodeAuthSMS


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('phoneNumber', 'fullname')


class CodeAuthSMSAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'time_expiry', 'is_active')


admin.site.register(Customer, CustomerAdmin)
admin.site.register(CodeAuthSMS, CodeAuthSMSAdmin)
