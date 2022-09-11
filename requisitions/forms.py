from django import forms
from requisitions.models import Request
from django.core.exceptions import ValidationError



class RequestsForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RequestsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    def clean_number(self):
        number = self.cleaned_data['number']
        if Request.objects.filter(number=number).exists():
            raise ValidationError(f"شماره درخواست {number} قبلا ثبت شده ")

class RequestsUpdateForm(RequestsForm):
    class Meta:
        model = Request
        fields = '__all__'
        exclude = ['number']