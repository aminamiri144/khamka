from django.db import models
from customers.models import Customer
import jdatetime
import random
# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    CATEGORY_TYPES = (
        ('1', 'دسته بندی نامه ها'),
        ('2', 'دسته بندی درخواست ها'),
    )

    subject = models.CharField(
        max_length=100, blank=False, null=False, verbose_name='نام دسته بندی')

    category_type = models.CharField(
        choices=CATEGORY_TYPES, blank=False, null=False, verbose_name='نوع دسته بندی',  max_length=100)

    description = models.TextField(
        blank=True, null=True, verbose_name='توضیحات')

    def __str__(self):
        return f'{self.subject}  ({self.get_category_type_display()})'


def generate_request_id():
    num = random.randint(10000, 99999)
    request_number = f'{num}'
    return request_number


class Request(models.Model):
    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = 'درخواست ها'

    REQUEST_STATUS = (
        ('1', 'ایجاد شده'),
        ('2', 'پیگیری در خانه ملت'),
        ('3', 'صدور نامه از طرف خانه ملت'),
        ('4', 'ارسال نامه به ارگان مربوطه'),
        ('5', 'در انتظار درخواست دهنده'),
        ('6', 'خاتمه یافته'),
    )

    RESULT_STATUS = (
        ('1', 'موفق'),
        ('2', 'بدون نتیجه'),
        ('3', 'نامشخص'),
    )


    CREATED_BY = (
        ('1', 'درخواست دهنده'),
        ('2', 'اپراتور خانه ملت'),
        ('3', 'نامشخص'),
    )

    number = models.CharField(verbose_name='شماره درخواست',
                              default=generate_request_id(), max_length=7)
    title = models.CharField(
        max_length=150, verbose_name='عنوان درخواست', blank=False, null=False)
    register_date = models.DateField(
        verbose_name='تاریخ ایجاد درخواست', blank=False, null=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, blank=True, null=True, verbose_name='درخواست دهنده')
    description = models.TextField(verbose_name='توضیحات')
    status = models.CharField(choices=REQUEST_STATUS, verbose_name='وضعیت',
                              default='1', blank=False, null=False, max_length=20)
    result = models.CharField(choices=RESULT_STATUS, verbose_name='نتیجه',
                              default='3', blank=False, null=False, max_length=20)

    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.PROTECT, verbose_name='دسته بندی')

    created_by = models.CharField(verbose_name='ایجاد شده توسط', blank=False, null=False, max_length=20, choices=CREATED_BY, default='3')

    @property
    def customer_name(self):
        return self.customer.fullname
    
    @property
    def result_d(self):
        return self.get_result_display()

    @property
    def status_d(self):
        return self.get_status_display()

    def __str__(self):
        return str(self.number)


class Survey(models.Model):

    SCORES = (
        ('1', 'بسیارضعیف'),
        ('2', 'ضعیف'),
        ('3', 'متوسط'),
        ('4', 'خوب'),
        ('5', 'بسیارخوب'),
        ('6', 'ثبت نشده'),
    )

    class Meta:
        verbose_name = 'نظرسنجی'
        verbose_name_plural = 'نظرسنجی ها'

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    request = models.ForeignKey(Request, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظرسنجی')
    score = models.CharField(choices=SCORES, blank=True, null=True, verbose_name='امتیاز', max_length=20, default='6')
