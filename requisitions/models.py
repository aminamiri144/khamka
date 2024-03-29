from django.db import models
from django_jalali.db import models as jmodels
from customers.models import Customer
from jdatetime import datetime as jd
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
        return f'{self.subject}'


def generate_request_id():
    num = random.randint(100000, 999999)
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
    objects = jmodels.jManager()
    number = models.CharField(verbose_name='شماره درخواست',
                              default=generate_request_id(), max_length=6)
    title = models.CharField(
        max_length=150, verbose_name='عنوان درخواست', blank=False, null=False)
    register_date = jmodels.jDateField(
        verbose_name='تاریخ ایجاد درخواست', blank=False, null=False)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, blank=False, null=False, verbose_name='درخواست دهنده')
    description = models.TextField(verbose_name='توضیحات')
    status = models.CharField(choices=REQUEST_STATUS, verbose_name='وضعیت',
                              default='1', blank=False, null=False, max_length=20)
    result = models.CharField(choices=RESULT_STATUS, verbose_name='نتیجه',
                              default='3', blank=False, null=False, max_length=20)

    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.PROTECT, verbose_name='دسته بندی')

    created_by = models.CharField(verbose_name='ایجاد شده توسط', blank=False,
                                  null=False, max_length=20, choices=CREATED_BY, default='3')
    updated_at = jmodels.jDateTimeField(
        verbose_name='تاریخ آخرین بروزرسانی', auto_now=True, blank=False, null=False)

    @property
    def customer_name(self):
        return self.customer.fullname

    @property
    def result_d(self):
        return self.get_result_display()

    @property
    def status_d(self):
        return self.get_status_display()

    def jd_register_date(self):
        jd_reg_date = str(self.register_date).replace('-','/')
        try:
            return jd_reg_date
        except:
            return 'ثبت نشده!'

    def __str__(self):
        return f"{self.customer} | {self.number} | {self.title}"

    
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
    date = models.DateTimeField(
        auto_now_add=True, verbose_name='تاریخ ثبت نظرسنجی')
    score = models.CharField(choices=SCORES, blank=True, null=True,
                             verbose_name='امتیاز', max_length=20, default='6')


def generate_attachments_path_file():
    y = jd.now().year
    m = jd.now().month
    path = f'attachments/{y}/{m}'
    return path


class Attachment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='درخواست')
    name = models.CharField(max_length=30, blank=False, null=False, verbose_name='نام یا توضیحات')
    filename = models.FileField(upload_to=generate_attachments_path_file(), blank=False, null=False, verbose_name='فایل')
    register_date = jmodels.jDateField(verbose_name='تاریخ ایجاد', blank=True, null=True)

    
    def jd_register_date(self):
        jd_reg_date = str(self.register_date).replace('-','/')
        try:
            return jd_reg_date
        except:
            return 'ثبت نشده!'

    def __str__(self):
        return f"{self.name}"



class Setting(models.Model):
    class Meta:
        verbose_name = 'تنظیم'
        verbose_name_plural = 'تنظیمات'

    key = models.CharField(max_length=50, verbose_name='عنوان')
    value = models.CharField(max_length=50, verbose_name='مقدار')