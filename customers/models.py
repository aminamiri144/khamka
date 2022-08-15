
from django.db import models


SEX = (
    (1, 'مرد'),
    (2, 'زن'),
    (3, 'حقوقی(سازمان)'),
)

# Create your models here.
class Customer(models.Model):
    class Meta:
        verbose_name = ('درخواست دهنده')
        verbose_name_plural = ('درخواست دهنده ها')

    phone_number = models.CharField(max_length=11, blank=False, null=False,verbose_name='تلفن همراه')
    fullname = models.CharField(max_length=255, blank=False, null=False, verbose_name='(یا نام سازمان)نام و نام خانوادگی')
    sex = models.CharField(choices=SEX,max_length=20, blank=False, null=False, verbose_name='جنسیت')
    phone = models.CharField(max_length=11, blank=True, null=True , verbose_name='تلفن ثابت')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='آدرس')
