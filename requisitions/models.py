from django.db import models
from customers.models import Customer

# Create your models here.


REQUEST_STATUS = (
    (1,'ایجاد شده'),
    (2,'پیگیری در خانه ملت'),
    (3,'صدور نامه از طرف خانه ملت'),
    (4,'ارسال نامه به ارگان مربوطه'),
    (5,'در انتظار درخواست دهنده'),
    (6,'خاتمه یافته'),
)

RESULT_STATUS = (
    (1,'موفق'),
    (2,'بدون نتیجه'),
    (3,'نامشخص'),
)


SCORES = (
    (1,'بسیارضعیف'),
    (2,'ضعیف'),
    (3,'متوسط'),
    (4,'خوب'),
    (5,'بسیارخوب'),
)


class Request(models.Model):
    class Meta:
        verbose_name='درخواست'
        verbose_name_plural='درخواست ها'

    number = models.BigAutoField(primary_key=True, verbose_name='شماره درخواست')
    title = models.CharField(max_length=150, verbose_name='عنوان درخواست', blank=False, null=False)
    register_date = models.DateField(verbose_name='تاریخ ایجاد درخواست', blank=False, null=False)
    description = models.TextField(verbose_name='توضیحات')
    status = models.CharField(choices=REQUEST_STATUS, verbose_name='وضعیت', default=1, blank=False, null=False)
    result = models.CharField(choices=RESULT_STATUS, verbose_name='نتیجه', default=3, blank=False, null=False)



class Survey(models.Model):
    class Meta:
        verbose_name='نظرسنجی'
        verbose_name_plural='نظرسنجی ها'

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    request = models.ForeignKey(Request, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظرسنجی')
    score = models.IntegerField(choices=SCORES,blank=True,null=True, verbose_name='امتیاز')