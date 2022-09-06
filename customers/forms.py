from dataclasses import field
from django import forms
from customers.models import Customer
from django.core.exceptions import ValidationError


def phoneNumbervalidator(value):
    if Customer.objects.filter(phoneNumber=value).exists():

        raise ValidationError(f"شماره تلفن {value} قبلا ثبت شده ")


class CustomerForm(forms.ModelForm):
    class Meta: 
        model = Customer
        fields = '__all__'

        error_messages = {
            'phoneNumber': {
                'exsist': "شماره تلفن همراه این کاربر قبلا ثبت شده!",
            },
        }


    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_phone_number(self):
        phoneNumber = self.cleaned_data['phoneNumber']
        if Customer.objects.filter(phoneNumber=phoneNumber).exists():
            raise ValidationError(f"شماره تلفن {phoneNumber} قبلا ثبت شده ")