from django.db import models
from requisitions.models import Request
from jdatetime import datetime as jd
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField



class Organ(models.Model):
    class Meta:
        verbose_name = 'سازمان'
        verbose_name_plural = 'سازمان ها'

    ORG_TYPES = (
        ('1', 'دولتی'),
        ('2', 'خصوصی'),
        ('3', 'شرکت یا کارخانه'),
        ('4', 'بانک و موسسات مالی'),
        ('5', 'نامشخص'),
    )

    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='نام سازمان')
    org_type = models.CharField(choices=ORG_TYPES, max_length=100, blank=False, null=False, verbose_name='نوع سازمان')
    decriptions = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    def __str__(self):
        return self.name


class LetterCategory(models.Model):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    subject = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='نام دسته بندی')

    description = models.TextField(
        blank=True, null=True, verbose_name='توضیحات')

    def __str__(self):
        return f'{self.subject}'



class Letter(models.Model):
    class Meta:
        verbose_name = 'نامه'
        verbose_name_plural = 'نامه ها'

    LETTER_STATUS = (
        ('1', 'در انتظار ارسال'),
        ('2', 'ارسال به دبیرخانه'),
        ('3', 'ارسال شده'),
        ('4', 'درحال بررسی'),
    )

    LETTER_TYPE = (
        ('1', 'ارسالی'),
        ('2', 'دریافتی'),
        ('3', 'جوابیه'),
    )

    letter_number = models.CharField(max_length=30, blank=False, null=False, verbose_name='شماره نامه')
    title = models.CharField(max_length=255, blank=False,null=False, verbose_name='موضوع نامه')
    request = models.ForeignKey(Request, blank=False, null=False, verbose_name='درخواست مرجع', on_delete=models.PROTECT)
    register_date = jmodels.jDateField(verbose_name='تاریخ نامه', blank=False, null=False)
    descrption = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    image = ResizedImageField(upload_to='lettersImage/', verbose_name='تصویر نامه', blank=True, null=True, quality=50)
    recepiant = models.ForeignKey(Organ, blank=True, null=True, verbose_name='گیرنده نامه', default='5', on_delete=models.SET_NULL)
    status = models.CharField(choices=LETTER_STATUS, blank=False, null=False, verbose_name='وضعیت نامه', max_length=30)
    status = models.CharField(choices=LETTER_TYPE, blank=False, null=False, verbose_name='نوع نامه', max_length=30)
    category = models.ForeignKey(LetterCategory, on_delete=models.PROTECT, verbose_name='دسته بندی', null=True, blank=True)
    
    def __str__(self):
        return f"{self.letter_number} {self.title}"
