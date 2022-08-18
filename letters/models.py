from django.db import models
from requisitions.models import Request
class Letter(models.Model):
    class Meta:
        verbose_name = 'نامه'
        verbose_name_plural = 'نامه ها'


    LETTER_STATUS = (
        ('1', 'در انتظار ارسال'),
        ('2', 'ارسال به دبیرخانه'),
        ('3', 'ارسال شده'),
    )

    letter_number = models.CharField(max_length=30, blank=False, null=False, verbose_name='شماره نامه')
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name='موضوع نامه')
    register_date = models.DateField(verbose_name='تاریخ نامه', blank=False, null=False)
    descrption = models.TextField(verbose_name='توضیحات', blank=True, null=True)
    image = models.ImageField(upload_to='lettersImage/', verbose_name='تصویر نامه', blank=True, null=True)
    recepiant = models.CharField(blank=True, max_length=50, null=True, verbose_name='گیرنده نامه')
    request = models.ForeignKey(Request, blank=False, null=False, verbose_name='درخواست مرجع', on_delete=models.PROTECT)
    status = models.CharField(choices=LETTER_STATUS, blank=False, null=False, verbose_name='وضعیت نامه', max_length=30)


    def __str__(self):
        return self.letter_number

    