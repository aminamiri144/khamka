from io import StringIO
from PIL import Image
from django import forms
from letters.models import Letter, Organ
from django.core.exceptions import ValidationError
from khamka.datetimeUtils import change_date_to_english


class LetterForm(forms.ModelForm):
    register_date = forms.CharField(label='تاریخ درخواست:')

    class Meta:
        model = Letter
        fields = [
            'recepiant',
            'letter_number',
            'title',
            'request',
            'register_date',
            'descrption',
            'image',
            'status',
            'letter_type',
            'category'
        ]

    def __init__(self, *args, **kwargs):
        super(LetterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['request'].disabled = True

   
    def clean_register_date(self):
        register_date = self.cleaned_data['register_date']
        try:
            register_date = change_date_to_english(register_date, 2)
        except:
            register_date = None
        return register_date

    # def clean_image(self):
    #     image_field = self.cleaned_data['image']
    #     image_file = StringIO(image_field)
    #     image = Image.open(image_file)
    #     w, h = image.size
    #     image = image.resize((w/2, h/2), Image.ANTIALIAS)
    #     image_file = StringIO()
    #     image.save(image_file, 'JPEG', quality=70)
    #     image_field.file = image_file
    #     return image_field


class OrganForm(forms.ModelForm):
    class Meta:
        model = Organ
        fields= '__all__'
    
    def __init__(self, *args, **kwargs):
        super(OrganForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'