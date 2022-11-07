from django import forms
from letters.models import Letter
from django.core.exceptions import ValidationError


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    # def clean_phone_number(self):
    #     phoneNumber = self.cleaned_data['phoneNumber']
    #     if Customer.objects.filter(phoneNumber=phoneNumber).exists():
    #         raise ValidationError(f"شماره تلفن {phoneNumber} قبلا ثبت شده ")