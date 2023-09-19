# Generated by Django 3.2 on 2023-09-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisitions', '0010_auto_20230919_1111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, verbose_name='عنوان')),
                ('value', models.CharField(max_length=50, verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'تنظیم',
                'verbose_name_plural': 'تنظیمات',
            },
        ),
        migrations.AlterField(
            model_name='request',
            name='number',
            field=models.CharField(default='968107', max_length=6, verbose_name='شماره درخواست'),
        ),
    ]
