
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Customer(AbstractUser):

    SEX = (
        ('1', 'مرد'),
        ('2', 'زن'),
        ('3', 'حقوقی(سازمان)'),
    )

    class Meta:
        verbose_name = ('درخواست دهنده')
        verbose_name_plural = ('درخواست دهنده ها')

    AbstractUser._meta.get_field('username').verbose_name = 'شماره تلفن همراه'
    AbstractUser._meta.get_field('first_name').verbose_name = 'نام'
    AbstractUser._meta.get_field('last_name').verbose_name = 'نام خانوادگی'
    code_meli= models.CharField(max_length=10, blank=True, null=True, verbose_name='کد ملی')
    sex = models.CharField(choices=SEX, max_length=20,
                           blank=False, null=False, verbose_name='جنسیت')
    phone = models.CharField(max_length=11, blank=True,
                             null=True, verbose_name='تلفن ثابت')
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='آدرس')


    def __str__(self):
        return self.first_name + ' ' + self.last_name