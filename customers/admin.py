from django.contrib import admin

# Register your models here.
from customers.models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name','last_name')

admin.site.register(Customer, CustomerAdmin)