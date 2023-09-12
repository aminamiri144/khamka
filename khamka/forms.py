from django import forms

SEX = (
        ('2', 'زن'),
        ('1', 'مرد'),
    )
class Customer_register_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(Customer_register_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    fullname = forms.CharField(label="نام و نام خانوادگی", max_length=40, required=False) 
    codemeli = forms.CharField(label="کد ملی", max_length=10, min_length=10, required=False)
    sex = forms.ChoiceField(choices=SEX ,label="جنسیت", required=False)


class request_register_form(forms.Form):
    def __init__(self, *args, **kwargs):
        super(request_register_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    title = forms.CharField(label="عنوان درخواست", max_length=100, required=False) 
    description = forms.TextInput()
