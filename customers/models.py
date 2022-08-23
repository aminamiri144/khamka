
from django.db import models


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

    phoneNumber = models.CharField(primary_key=True ,max_length=11, verbose_name='شماره تلفن همراه', unique=True)
    fullname = models.CharField(max_length=50, blank=False, null=False, verbose_name='نام و نام خانوادگی')
    organ = models.CharField(max_length=100, blank=True, null=True, verbose_name='سازمان یا شرکت')
    code_meli= models.CharField(max_length=10, blank=True, null=True, verbose_name='کد ملی')
    sex = models.CharField(choices=SEX, max_length=20,blank=False, null=False, verbose_name='جنسیت')
    phone = models.CharField(max_length=11, blank=True,null=True, verbose_name='تلفن ثابت')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='آدرس')
    register_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظرسنجی')

    def __str__(self):
        return self.fullname