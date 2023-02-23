from django import forms
import customers
from requisitions.models import Request, Attachment
from django.core.exceptions import ValidationError
from khamka.datetimeUtils import change_date_to_english

class RequestsForm(forms.ModelForm):
    register_date = forms.CharField(label='تاریخ درخواست:')
    class Meta:
        model = Request
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequestsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['customer'].disabled = True
    
    def clean_number(self):
        number = self.cleaned_data['number']
        if Request.objects.filter(number=number).exists():
            raise ValidationError(f".شماره درخواست {number} قبلا ثبت شده! یک شماره دلخواه 5 رقمی وارد کنید ")
        else:
            return number
    
    def clean_register_date(self):
        register_date = self.cleaned_data['register_date']
        try:
            register_date = change_date_to_english(register_date, 2)
        except:
            register_date = None
        return register_date

class RequestsUpdateForm(forms.ModelForm):
    # register_date = forms.CharField(label='تاریخ درخواست:')

    class Meta:
        model = Request
        fields = '__all__'
        exclude = ['description', 'register_date']

    
    def __init__(self, *args, **kwargs):
        super(RequestsUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['title'].disabled = True
        self.fields['number'].disabled = True
        self.fields['customer'].disabled = True

    def clean_register_date(self):
        register_date = self.cleaned_data['register_date']
        try:
            register_date = change_date_to_english(register_date, 2)
        except:
            register_date = register_date
        return register_date


class AttachmentForm(forms.ModelForm):
    register_date = forms.CharField(label='تاریخ افزودن پیوست:')

    class Meta:
        model = Attachment
        fields = '__all__'
        
        
    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['request'].disabled = True

    def clean_register_date(self):
        register_date = self.cleaned_data['register_date']
        try:
            register_date = change_date_to_english(register_date, 2)
        except:
            register_date = register_date
        return register_date


class RequestForm2(forms.ModelForm):
    register_date = forms.CharField(label='تاریخ درخواست:')
    class Meta:
        model = Request
        fields = '__all__'
        exclude = ['customer']

    def __init__(self, *args, **kwargs):
        super(RequestForm2, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean_number(self):
        number = self.cleaned_data['number']
        if Request.objects.filter(number=number).exists():
            raise ValidationError(f".شماره درخواست {number} قبلا ثبت شده! یک شماره دلخواه 6 رقمی وارد کنید ")
        else:
            return number
    
    def clean_register_date(self):
        register_date = self.cleaned_data['register_date']
        try:
            register_date = change_date_to_english(register_date, 2)
        except:
            register_date = None
        return register_date