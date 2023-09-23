from django import forms
from khamka.utils import validate_code_meli
from django.core.exceptions import ValidationError


from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


SEX = (
        ('2', 'زن'),
        ('1', 'مرد'),
    )

class Mobile_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Mobile_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    mobile = forms.CharField(label='شماره موبایل', max_length=11, required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)



class Customer_register_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Customer_register_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    fullname = forms.CharField(label="نام و نام خانوادگی", max_length=40, required=False) 
    codemeli = forms.CharField(label="کد ملی", max_length=10, min_length=10, required=False)
    sex = forms.ChoiceField(choices=SEX ,label="جنسیت", required=False)

    def clean_codemeli(self):
        codemeli = self.cleaned_data['codemeli']
        if len(codemeli) > 1 and not validate_code_meli(codemeli):
            raise ValidationError(f"کد ملی وارد شده معتبر نیست")


class request_register_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(request_register_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    title = forms.CharField(label="عنوان درخواست", max_length=100, required=False) 
    description = forms.TextInput()
