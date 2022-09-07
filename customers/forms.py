from django import forms
from customers.models import Customer
from django.core.exceptions import ValidationError




class CustomerForm(forms.ModelForm):
    class Meta: 
        model = Customer
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_phone_number(self):
        phoneNumber = self.cleaned_data['phoneNumber']
        if Customer.objects.filter(phoneNumber=phoneNumber).exists():
            raise ValidationError(f"شماره تلفن {phoneNumber} قبلا ثبت شده ")

class CustomerUpdateForm(CustomerForm):
    class Meta: 
        model = Customer
        fields = '__all__'
        exclude = ['id']