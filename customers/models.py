
from django.db import models
from jdatetime import datetime as jd


# Create your models here.
class Customer(models.Model):
    class Meta:
        verbose_name = ('درخواست دهنده')
        verbose_name_plural = ('درخواست دهنده ها')

    SEX = (
        ('1', 'مرد'),
        ('2', 'زن'),
        ('3', 'حقوقی(سازمان)'),
    )
    phoneNumber = models.CharField(blank=False, null=False ,max_length=11, verbose_name='شماره تلفن همراه')
    fullname = models.CharField(max_length=50, blank=False, null=False, verbose_name='نام و نام خانوادگی')
    organ = models.CharField(max_length=100, blank=True, null=True, verbose_name='سازمان یا شرکت')
    code_meli= models.CharField(max_length=10, blank=True, null=True, verbose_name='کد ملی')
    sex = models.CharField(choices=SEX, max_length=20,blank=False, null=False, verbose_name='جنسیت')
    phone = models.CharField(max_length=11, blank=True,null=True, verbose_name='تلفن ثابت')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='آدرس')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظرسنجی')

    def jd_register_date(self):
        try:
            return jd.fromgregorian(
                date=self.register_date,
            ).strftime('%Y/%m/%d')
        except:
            return 'ثبت نشده!'

    def codeMeli(self):
        if self.code_meli is None:
            return "ثبت نشده"
        else:
            return self.code_meli
    
    def organ_name(self):
        if self.organ is None:
            return "ثبت نشده"
        else:
            return self.organ

    def phonee(self):
        if self.phone is None:
            return "ثبت نشده"
        else:
            return self.phone

    def __str__(self):
        return self.fullname



class CodeAuthSMS(models.Model):
    class Meta:
        verbose_name = ('کد اعتبار سنجی')
        verbose_name_plural = ('کد های اعتبار سنجی')

    phone = models.CharField(verbose_name='شماره تلفن همراه', max_length=11)
    code = models.IntegerField(verbose_name='کد احراز هویت')
    is_active = models.BooleanField(verbose_name='فعال بودن کد')
    time_expiry = models.CharField(verbose_name='زمان انقضا', max_length=30)

    def __str__(self):
        return f'{self.phone} | {self.code} | {self.is_active} | {self.time_expiry}'